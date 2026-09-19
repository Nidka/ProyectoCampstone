-- Módulo de Registro de Gastos y Comprobantes (LIZAR SRL)
-- Reutiliza las tablas existentes: programacionviaje (viajes) y cliente.

CREATE TABLE IF NOT EXISTS gasto (
    id            SERIAL PRIMARY KEY,
    viaje_id      INTEGER NOT NULL REFERENCES programacionviaje (id_viaje),
    cliente_id    INTEGER NOT NULL REFERENCES cliente (id_cliente),
    monto         NUMERIC(10, 2) NOT NULL CHECK (monto > 0),
    fecha         DATE NOT NULL,
    estado        VARCHAR(20) NOT NULL DEFAULT 'Registrado'
                  CHECK (estado IN ('Registrado', 'Pagado', 'Sustentado')),
    creado_por    VARCHAR(100) NOT NULL,
    creado_en     TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS comprobante (
    id             SERIAL PRIMARY KEY,
    gasto_id       INTEGER NOT NULL REFERENCES gasto (id),
    archivo_url    VARCHAR(500) NOT NULL,
    tipo_archivo   VARCHAR(10) NOT NULL CHECK (tipo_archivo IN ('imagen', 'pdf')),
    estado         VARCHAR(20) NOT NULL DEFAULT 'Pendiente'
                   CHECK (estado IN ('Pendiente', 'Aprobado', 'Rechazado')),
    motivo_rechazo TEXT,
    aprobado_por   VARCHAR(100),
    aprobado_en    TIMESTAMP,
    creado_en      TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_gasto_viaje_id ON gasto (viaje_id);
CREATE INDEX IF NOT EXISTS idx_comprobante_gasto_id ON comprobante (gasto_id);
