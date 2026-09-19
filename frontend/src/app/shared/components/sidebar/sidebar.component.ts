import { Component, inject, output } from '@angular/core';
import { CrudService } from '../../../core/services/crud.service';

interface NavLink {
  key: string;
  label: string;
  group: string;
  svgPath: string;
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css'],
})
export class SidebarComponent {
  crud = inject(CrudService);

  activeKey = 'dash';
  readonly viewChange = output<string>();

  setActive(key: string): void {
    this.activeKey = key;
    this.viewChange.emit(key);
  }

  count(nk: string): number {
    const c = this.crud.cruds.find(x => x.nk === nk);
    return c ? this.crud.getItems(c.key).length : 0;
  }

  readonly groups: { name: string; links: NavLink[] }[] = [
    {
      name: 'General',
      links: [
        { key: 'dash',         label: 'Panel general',   group: 'General',     svgPath: 'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z' },
        { key: 'presentacion', label: 'Presentación',    group: 'General',     svgPath: 'M2 3h20v14H2z M8 21h8 M12 17v4' },
      ],
    },
    // Los módulos de Maestros, Operaciones, Logística y Finanzas no forman
    // parte de los requerimientos de esta iteración (solo Registro de Gasto,
    // Comprobante de Pago y Aprobación) y se ocultan del menú.
    {
      name: 'Gastos',
      links: [
        { key: 'gasto_nuevo',      label: 'Registrar gasto',   group: 'Gastos', svgPath: 'M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6' },
        { key: 'gasto_comprobante',label: 'Comprobante de pago',group: 'Gastos', svgPath: 'M14 2H6a2 2 0 0 0-2 2v16h16V8z M14 2v6h6 M9 15l2 2 4-4' },
        { key: 'gasto_aprobacion', label: 'Aprobación',        group: 'Gastos', svgPath: 'M9 11l3 3L22 4 M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11' },
      ],
    },
  ];
}
