package config

import (
	"bufio"
	"os"
	"strings"
)

// Config agrupa los parámetros de arranque del servicio, leídos de variables
// de entorno (o de un archivo .env local si existe).
type Config struct {
	Port        string
	DatabaseURL string
	UploadsDir  string
}

// Load lee un .env si existe (sin sobreescribir variables ya definidas en el
// entorno) y arma la configuración con valores por defecto razonables.
func Load() Config {
	loadDotEnv(".env")

	return Config{
		Port:        getEnv("PORT", "8081"),
		DatabaseURL: getEnv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable"),
		UploadsDir:  getEnv("UPLOADS_DIR", "./uploads"),
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func loadDotEnv(path string) {
	f, err := os.Open(path)
	if err != nil {
		return
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		key, value, found := strings.Cut(line, "=")
		if !found {
			continue
		}
		key = strings.TrimSpace(key)
		value = strings.Trim(strings.TrimSpace(value), `"'`)
		if _, exists := os.LookupEnv(key); !exists {
			os.Setenv(key, value)
		}
	}
}
