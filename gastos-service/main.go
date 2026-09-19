package main

import (
	"log"
	"net/http"
	"os"

	"gastos-service/internal/config"
	"gastos-service/internal/db"
	"gastos-service/internal/handlers"
)

func main() {
	cfg := config.Load()

	pool, err := db.Connect(cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("no se pudo conectar a la base de datos: %v", err)
	}
	defer pool.Close()

	if err := db.RunMigrations(pool, "migrations"); err != nil {
		log.Fatalf("error aplicando migraciones: %v", err)
	}

	if err := os.MkdirAll(cfg.UploadsDir, 0o755); err != nil {
		log.Fatalf("no se pudo crear el directorio de comprobantes: %v", err)
	}

	mux := http.NewServeMux()
	handlers.New(pool, cfg).Register(mux)

	log.Printf("gastos-service escuchando en :%s", cfg.Port)
	if err := http.ListenAndServe(":"+cfg.Port, handlers.CORS(mux)); err != nil {
		log.Fatal(err)
	}
}
