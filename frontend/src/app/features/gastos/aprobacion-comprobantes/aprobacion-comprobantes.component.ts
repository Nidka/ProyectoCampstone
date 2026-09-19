import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { timeout } from 'rxjs';
import { CrudService } from '../../../core/services/crud.service';
import { GastosApiService, RolSimulado } from '../../../core/services/gastos-api.service';
import { ToastService } from '../../../core/services/toast.service';
import { Comprobante, Gasto } from '../../../core/models/gasto.model';
import { HTTP_TIMEOUT_MS, mensajeError } from '../../../core/utils/error-messages';

@Component({
  selector: 'app-aprobacion-comprobantes',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './aprobacion-comprobantes.component.html',
})
export class AprobacionComprobantesComponent implements OnInit {
  api = inject(GastosApiService);
  private crud = inject(CrudService);
  private toast = inject(ToastService);

  pendientes = signal<Comprobante[]>([]);
  gastosMap = signal<Record<number, Gasto>>({});
  loading = signal(false);

  /** comprobante que se está por rechazar; null = modal cerrado */
  rechazando = signal<Comprobante | null>(null);
  motivo = '';
  motivoError = '';

  readonly hayPendientes = computed(() => this.pendientes().length > 0);

  get rolActual(): RolSimulado {
    return this.api.currentUser().rol;
  }

  ngOnInit(): void {
    if (this.crud.getItems('cliente').length === 0) this.crud.loadList('cliente');
    this.load();
  }

  setRol(rol: RolSimulado): void {
    this.api.currentUser.update(u => ({ ...u, rol }));
  }

  load(): void {
    this.loading.set(true);
    this.api.get<Comprobante[]>('/comprobantes?estado=Pendiente').pipe(timeout(HTTP_TIMEOUT_MS)).subscribe({
      next: rows => {
        this.pendientes.set(rows);
        this.loading.set(false);
      },
      error: err => {
        this.loading.set(false);
        this.toast.show(mensajeError(err), '', 'err');
      },
    });

    this.api.get<Gasto[]>('/gastos').pipe(timeout(HTTP_TIMEOUT_MS)).subscribe({
      next: rows => {
        const map: Record<number, Gasto> = {};
        rows.forEach(g => (map[g.id] = g));
        this.gastosMap.set(map);
      },
      error: err => this.toast.show(mensajeError(err), '', 'err'),
    });
  }

  gastoDe(c: Comprobante): Gasto | undefined {
    return this.gastosMap()[c.gasto_id];
  }

  clienteNombre(clienteId: number): string {
    const cliente = this.crud.getItems('cliente').find((c: Record<string, unknown>) => c['id_cliente'] === clienteId);
    return (cliente?.['razon_social'] as string) ?? `Cliente #${clienteId}`;
  }

  fileUrl(archivoUrl: string): string {
    return this.api.fileUrl(archivoUrl);
  }

  fechaCorta(fecha: string | undefined): string {
    return fecha ? fecha.slice(0, 10) : '—';
  }

  aprobar(c: Comprobante): void {
    this.api.post(`/comprobantes/${c.id}/aprobar`, {}).pipe(timeout(HTTP_TIMEOUT_MS)).subscribe({
      next: () => {
        this.toast.show('Comprobante aprobado. El gasto quedó como "Sustentado".', '', 'ok');
        this.load();
      },
      error: err => this.toast.show(mensajeError(err), '', 'err'),
    });
  }

  abrirRechazo(c: Comprobante): void {
    this.rechazando.set(c);
    this.motivo = '';
    this.motivoError = '';
  }

  cancelarRechazo(): void {
    this.rechazando.set(null);
    this.motivo = '';
    this.motivoError = '';
  }

  confirmarRechazo(): void {
    const c = this.rechazando();
    if (!c) return;

    if (!this.motivo.trim()) {
      this.motivoError = 'Debes indicar un motivo para rechazar el comprobante.';
      return;
    }

    this.api.post(`/comprobantes/${c.id}/rechazar`, { motivo_rechazo: this.motivo.trim() }).pipe(timeout(HTTP_TIMEOUT_MS)).subscribe({
      next: () => {
        this.toast.show('Comprobante rechazado. El gasto volvió a estado "Registrado".', '', 'ok');
        this.cancelarRechazo();
        this.load();
      },
      error: err => this.toast.show(mensajeError(err), '', 'err'),
    });
  }
}
