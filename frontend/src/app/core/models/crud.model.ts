/** Definición de un campo de formulario CRUD */
export interface CrudField {
  id: string;
  l: string;               // label
  tp: 'text' | 'number' | 'textarea' | 'email';
  req?: boolean;
  half?: boolean;          // ocupa la mitad del grid
  placeholder?: string;
  rule?: (v: string) => boolean;
  msg?: string;            // mensaje de error de regla
}

/** Definición completa de un módulo CRUD */
export interface CrudDef {
  key: string;
  title: string;
  route: string;           // ruta API: /conductores
  nk: string;              // sidebar badge id suffix
  group: 'Maestros' | 'Operaciones' | 'Logística' | 'Finanzas';
  desc: string;
  fields: CrudField[];
  pay: (form: Record<string, HTMLInputElement | HTMLTextAreaElement>) => Record<string, unknown>;
  cols: string[];
  row: (item: Record<string, unknown>) => string[];
}

/** Toast */
export type ToastType = 'ok' | 'err' | 'info' | 'warn';
export interface Toast {
  id: number;
  title: string;
  msg: string;
  type: ToastType;
}

/** Nav item para sidebar */
export interface NavItem {
  key: string;
  label: string;
  icon: string;            // SVG path o elemento
  group: string;
}
