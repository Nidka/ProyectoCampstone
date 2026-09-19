package handlers

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"gastos-service/internal/models"
)

const maxUploadSize = 10 << 20 // 10 MB

// uploadComprobante implementa RF-4 (adjuntar comprobante a un gasto),
// RF-6 (rechazar formatos que no sean imagen o PDF) y RF-5 (el gasto pasa
// a Pagado automáticamente al adjuntar un comprobante).
func (h *Handler) uploadComprobante(w http.ResponseWriter, r *http.Request) {
	gastoID, err := strconv.Atoi(r.PathValue("id"))
	if err != nil || gastoID <= 0 {
		writeError(w, http.StatusBadRequest, "id de gasto inválido")
		return
	}

	ctx := context.Background()

	var gastoExiste bool
	if err := h.DB.QueryRow(ctx, `SELECT EXISTS(SELECT 1 FROM gasto WHERE id = $1)`, gastoID).Scan(&gastoExiste); err != nil {
		writeError(w, http.StatusInternalServerError, "error validando el gasto")
		return
	}
	if !gastoExiste {
		writeError(w, http.StatusNotFound, "el gasto indicado no existe")
		return
	}

	r.Body = http.MaxBytesReader(w, r.Body, maxUploadSize)
	if err := r.ParseMultipartForm(maxUploadSize); err != nil {
		writeError(w, http.StatusBadRequest, "el archivo es demasiado grande o el formulario es inválido")
		return
	}

	file, header, err := r.FormFile("archivo")
	if err != nil {
		writeError(w, http.StatusBadRequest, "adjunta un archivo en el campo 'archivo'")
		return
	}
	defer file.Close()

	// RF-6: se valida por contenido real del archivo, no solo por su extensión.
	buf := make([]byte, 512)
	n, _ := file.Read(buf)
	contentType := http.DetectContentType(buf[:n])
	if _, err := file.Seek(0, io.SeekStart); err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo leer el archivo")
		return
	}

	tipoArchivo, ok := clasificarTipoArchivo(contentType, header.Filename)
	if !ok {
		writeError(w, http.StatusUnprocessableEntity, "solo se permiten archivos de imagen o PDF")
		return
	}

	ext := filepath.Ext(header.Filename)
	filename := fmt.Sprintf("gasto-%d-%d%s", gastoID, time.Now().UnixNano(), ext)
	destPath := filepath.Join(h.Cfg.UploadsDir, filename)

	dest, err := os.Create(destPath)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo guardar el archivo")
		return
	}
	defer dest.Close()

	if _, err := io.Copy(dest, file); err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo guardar el archivo")
		return
	}

	// RNF-3: el comprobante no se edita una vez guardado; cada subida crea un
	// registro nuevo con su propio archivo.
	archivoURL := "/uploads/" + filename

	tx, err := h.DB.Begin(ctx)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo iniciar la operación")
		return
	}
	defer tx.Rollback(ctx)

	var c models.Comprobante
	err = tx.QueryRow(ctx, `
		INSERT INTO comprobante (gasto_id, archivo_url, tipo_archivo, estado, creado_en)
		VALUES ($1, $2, $3, 'Pendiente', now())
		RETURNING id, gasto_id, archivo_url, tipo_archivo, estado, motivo_rechazo, aprobado_por, aprobado_en, creado_en
	`, gastoID, archivoURL, tipoArchivo).Scan(
		&c.ID, &c.GastoID, &c.ArchivoURL, &c.TipoArchivo, &c.Estado,
		&c.MotivoRechazo, &c.AprobadoPor, &c.AprobadoEn, &c.CreadoEn,
	)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo registrar el comprobante")
		return
	}

	// RF-5: adjuntar un comprobante cambia el gasto a "Pagado".
	if _, err := tx.Exec(ctx, `UPDATE gasto SET estado = 'Pagado' WHERE id = $1`, gastoID); err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo actualizar el estado del gasto")
		return
	}

	if err := tx.Commit(ctx); err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo confirmar la operación")
		return
	}

	writeJSON(w, http.StatusCreated, c)
}

func clasificarTipoArchivo(contentType, filename string) (string, bool) {
	lower := strings.ToLower(filename)
	switch {
	case strings.HasPrefix(contentType, "image/"):
		return "imagen", true
	case contentType == "application/pdf", strings.HasSuffix(lower, ".pdf"):
		return "pdf", true
	case strings.HasSuffix(lower, ".jpg"), strings.HasSuffix(lower, ".jpeg"),
		strings.HasSuffix(lower, ".png"), strings.HasSuffix(lower, ".webp"):
		return "imagen", true
	default:
		return "", false
	}
}

// listComprobantes soporta la pantalla de aprobación (filtrando por
// ?estado=Pendiente); la consulta general no es alcance de esta iteración.
func (h *Handler) listComprobantes(w http.ResponseWriter, r *http.Request) {
	estado := r.URL.Query().Get("estado")
	ctx := context.Background()

	query := `
		SELECT id, gasto_id, archivo_url, tipo_archivo, estado, motivo_rechazo, aprobado_por, aprobado_en, creado_en
		FROM comprobante`
	args := []any{}
	if estado != "" {
		query += ` WHERE estado = $1`
		args = append(args, estado)
	}
	query += ` ORDER BY creado_en DESC LIMIT 200`

	rows, err := h.DB.Query(ctx, query, args...)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo listar los comprobantes")
		return
	}
	defer rows.Close()

	out := []models.Comprobante{}
	for rows.Next() {
		var c models.Comprobante
		if err := rows.Scan(&c.ID, &c.GastoID, &c.ArchivoURL, &c.TipoArchivo, &c.Estado, &c.MotivoRechazo, &c.AprobadoPor, &c.AprobadoEn, &c.CreadoEn); err != nil {
			writeError(w, http.StatusInternalServerError, "error leyendo los comprobantes")
			return
		}
		out = append(out, c)
	}
	writeJSON(w, http.StatusOK, out)
}

type aprobarRequest struct {
	AprobadoPor string `json:"aprobado_por"`
}

// aprobarComprobante implementa RF-7 (aprobar) para el rol Encargado de
// Logística, y hace avanzar el gasto a "Sustentado".
func (h *Handler) aprobarComprobante(w http.ResponseWriter, r *http.Request) {
	nombre, autorizado := requireLogistica(r)
	if !autorizado {
		writeError(w, http.StatusForbidden, "solo el Encargado de Logística puede aprobar comprobantes")
		return
	}

	id, err := strconv.Atoi(r.PathValue("id"))
	if err != nil {
		writeError(w, http.StatusBadRequest, "id inválido")
		return
	}

	var req aprobarRequest
	_ = json.NewDecoder(r.Body).Decode(&req) // cuerpo opcional
	if req.AprobadoPor != "" {
		nombre = req.AprobadoPor
	}

	ctx := context.Background()
	tx, err := h.DB.Begin(ctx)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo iniciar la operación")
		return
	}
	defer tx.Rollback(ctx)

	var gastoID int
	err = tx.QueryRow(ctx, `
		UPDATE comprobante SET estado = 'Aprobado', aprobado_por = $1, aprobado_en = now()
		WHERE id = $2 RETURNING gasto_id
	`, nombre, id).Scan(&gastoID)
	if err != nil {
		writeError(w, http.StatusNotFound, "comprobante no encontrado")
		return
	}

	if _, err := tx.Exec(ctx, `UPDATE gasto SET estado = 'Sustentado' WHERE id = $1`, gastoID); err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo actualizar el gasto")
		return
	}

	if err := tx.Commit(ctx); err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo confirmar la operación")
		return
	}

	writeJSON(w, http.StatusOK, map[string]string{"status": "aprobado"})
}

type rechazarRequest struct {
	MotivoRechazo string `json:"motivo_rechazo"`
	AprobadoPor   string `json:"aprobado_por"`
}

// rechazarComprobante implementa RF-8 (motivo obligatorio) y RF-9 (el gasto
// vuelve a "Registrado").
func (h *Handler) rechazarComprobante(w http.ResponseWriter, r *http.Request) {
	nombre, autorizado := requireLogistica(r)
	if !autorizado {
		writeError(w, http.StatusForbidden, "solo el Encargado de Logística puede rechazar comprobantes")
		return
	}

	id, err := strconv.Atoi(r.PathValue("id"))
	if err != nil {
		writeError(w, http.StatusBadRequest, "id inválido")
		return
	}

	var req rechazarRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "cuerpo inválido")
		return
	}
	if strings.TrimSpace(req.MotivoRechazo) == "" {
		writeError(w, http.StatusBadRequest, "motivo_rechazo es obligatorio")
		return
	}
	if req.AprobadoPor != "" {
		nombre = req.AprobadoPor
	}

	ctx := context.Background()
	tx, err := h.DB.Begin(ctx)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo iniciar la operación")
		return
	}
	defer tx.Rollback(ctx)

	var gastoID int
	err = tx.QueryRow(ctx, `
		UPDATE comprobante SET estado = 'Rechazado', motivo_rechazo = $1, aprobado_por = $2, aprobado_en = now()
		WHERE id = $3 RETURNING gasto_id
	`, req.MotivoRechazo, nombre, id).Scan(&gastoID)
	if err != nil {
		writeError(w, http.StatusNotFound, "comprobante no encontrado")
		return
	}

	if _, err := tx.Exec(ctx, `UPDATE gasto SET estado = 'Registrado' WHERE id = $1`, gastoID); err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo actualizar el gasto")
		return
	}

	if err := tx.Commit(ctx); err != nil {
		writeError(w, http.StatusInternalServerError, "no se pudo confirmar la operación")
		return
	}

	writeJSON(w, http.StatusOK, map[string]string{"status": "rechazado"})
}
