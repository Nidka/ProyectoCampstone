import { Component, inject, OnInit, ViewChild, signal } from '@angular/core';
import { CrudService } from '../../core/services/crud.service';
import { ApiService } from '../../core/services/api.service';
import { GastosApiService } from '../../core/services/gastos-api.service';
import { Gasto, Comprobante } from '../../core/models/gasto.model';
import { SidebarComponent } from '../../shared/components/sidebar/sidebar.component';
import { TopbarComponent } from '../../shared/components/topbar/topbar.component';
import { ToastComponent } from '../../shared/components/toast/toast.component';
import { PresentationComponent } from '../presentation/presentation.component';
import { GastoFormComponent } from '../gastos/gasto-form/gasto-form.component';
import { ComprobanteUploadComponent } from '../gastos/comprobante-upload/comprobante-upload.component';
import { AprobacionComprobantesComponent } from '../gastos/aprobacion-comprobantes/aprobacion-comprobantes.component';

interface AccesoRapido { key: string; label: string; desc: string; svgPath: string; }

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    SidebarComponent, TopbarComponent, ToastComponent, PresentationComponent,
    GastoFormComponent, ComprobanteUploadComponent, AprobacionComprobantesComponent,
  ],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {
  crud = inject(CrudService);
  api  = inject(ApiService);
  private gastosApi = inject(GastosApiService);

  activeView = 'dash';

  // Solo se muestran los accesos de esta iteración (Registro de Gasto,
  // Comprobante de Pago y Aprobación); el resto de módulos del proyecto base
  // no están especificados en los requerimientos y quedan ocultos.
  readonly accesos: AccesoRapido[] = [
    { key: 'gasto_nuevo', label: 'Registrar gasto', desc: 'Registra un gasto adicional de viaje', svgPath: 'M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6' },
    { key: 'gasto_comprobante', label: 'Comprobante de pago', desc: 'Adjunta el comprobante de un gasto', svgPath: 'M14 2H6a2 2 0 0 0-2 2v16h16V8z M14 2v6h6 M9 15l2 2 4-4' },
    { key: 'gasto_aprobacion', label: 'Aprobación', desc: 'Aprueba o rechaza comprobantes pendientes', svgPath: 'M9 11l3 3L22 4 M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11' },
  ];

  gastos = signal<Gasto[]>([]);
  comprobantesPendientes = signal<Comprobante[]>([]);

  get totalRegistrados(): number { return this.gastos().filter(g => g.estado === 'Registrado').length; }
  get totalPagados(): number { return this.gastos().filter(g => g.estado === 'Pagado').length; }
  get totalSustentados(): number { return this.gastos().filter(g => g.estado === 'Sustentado').length; }
  get totalPendientes(): number { return this.comprobantesPendientes().length; }

  ngOnInit(): void {
    this.api.checkHealth();
    this.crud.refreshAll();
    this.loadResumenGastos();
  }

  private loadResumenGastos(): void {
    this.gastosApi.get<Gasto[]>('/gastos').subscribe({ next: rows => this.gastos.set(rows) });
    this.gastosApi.get<Comprobante[]>('/comprobantes?estado=Pendiente').subscribe({ next: rows => this.comprobantesPendientes.set(rows) });
  }

  @ViewChild(SidebarComponent) sidebar?: SidebarComponent;

  setView(key: string): void {
    this.activeView = key;
    if (this.sidebar) this.sidebar.activeKey = key;
  }
}
