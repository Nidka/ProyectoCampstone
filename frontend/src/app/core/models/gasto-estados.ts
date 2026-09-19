import { EstadoComprobante, EstadoGasto } from './gasto.model';

/** Etiquetas y colores de estado — copy exacto de UX writing, no reformular. */
export const ESTADO_GASTO_LABEL: Record<EstadoGasto, string> = {
  Registrado: 'Registrado',
  Pagado: 'Pagado',
  Sustentado: 'Sustentado',
};

export const ESTADO_GASTO_CLASS: Record<EstadoGasto, string> = {
  Registrado: 'lbl-n', // Gris
  Pagado: 'lbl-info', // Azul
  Sustentado: 'lbl-ok', // Verde
};

export const ESTADO_COMPROBANTE_LABEL: Record<EstadoComprobante, string> = {
  Pendiente: 'Pendiente de aprobación',
  Aprobado: 'Aprobado',
  Rechazado: 'Rechazado',
};

export const ESTADO_COMPROBANTE_CLASS: Record<EstadoComprobante, string> = {
  Pendiente: 'lbl-warn', // Amarillo
  Aprobado: 'lbl-ok', // Verde
  Rechazado: 'lbl-err', // Rojo
};
