package db

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"sort"

	"github.com/jackc/pgx/v5/pgxpool"
)

// Connect abre un pool de conexiones contra PostgreSQL.
func Connect(databaseURL string) (*pgxpool.Pool, error) {
	return pgxpool.New(context.Background(), databaseURL)
}

// RunMigrations ejecuta, en orden alfabético, todos los .sql de dir.
// Las migraciones usan CREATE TABLE IF NOT EXISTS, por lo que son idempotentes.
func RunMigrations(pool *pgxpool.Pool, dir string) error {
	entries, err := os.ReadDir(dir)
	if err != nil {
		return err
	}

	var files []string
	for _, e := range entries {
		if !e.IsDir() && filepath.Ext(e.Name()) == ".sql" {
			files = append(files, filepath.Join(dir, e.Name()))
		}
	}
	sort.Strings(files)

	for _, f := range files {
		contents, err := os.ReadFile(f)
		if err != nil {
			return fmt.Errorf("leyendo migración %s: %w", f, err)
		}
		if _, err := pool.Exec(context.Background(), string(contents)); err != nil {
			return fmt.Errorf("aplicando migración %s: %w", f, err)
		}
	}
	return nil
}
