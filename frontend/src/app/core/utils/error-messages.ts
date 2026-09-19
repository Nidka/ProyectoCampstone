import { TimeoutError } from 'rxjs';

/** Copy exacto de UX writing (RNF-1) — no reformular ni traducir. */
export const MSG_ERROR_RED = 'No pudimos guardar la información. Intenta de nuevo en unos segundos.';
export const MSG_TIMEOUT = 'La operación está tardando más de lo normal. Verifica tu conexión e intenta otra vez.';

/** Tiempo máximo de espera antes de considerar la operación colgada. */
export const HTTP_TIMEOUT_MS = 8000;

export function mensajeError(err: unknown): string {
  if (err instanceof TimeoutError) return MSG_TIMEOUT;
  return MSG_ERROR_RED;
}
