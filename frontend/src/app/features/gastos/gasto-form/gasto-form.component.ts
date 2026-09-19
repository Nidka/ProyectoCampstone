import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { timeout } from 'rxjs';
import { CrudService } from '../../../core/services/crud.service';
import { GastosApiService } from '../../../core/services/gastos-api.service';
import { ToastService } from '../../../core/services/toast.service';
import { Gasto } from '../../../core/models/gasto.model';
import { ESTADO_GASTO_CLASS, ESTADO_GASTO_LABEL } from '../../../core/models/gasto-estados';
import { HTTP_TIMEOUT_MS, mensajeError } from '../../../core/utils/error-messages';

@Component({
  selector: 'app-gasto-form',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './gasto-form.component.html',
})
export class GastoFormComponent implements OnInit {
  private crud = inject(CrudService);
  private api = inject(GastosApiService);
  private toast = inject(ToastService);

  readonly estadoLabel = ESTADO_GASTO_LABEL;
  readonly estadoClass = ESTADO_GASTO_CLASS;

  viajeId = '';
  clienteId = '';
  monto = '';
  fecha = new Date().toISOString().slice(0, 10);
  saving = signal(false);

  viajeError = '';
  clienteError = '';
  montoError = '';
  fechaError = '';

  get viajes(): Record<string, unknown>[] {
    return this.crud.getItems('viaje');
  }

  get clientes(): Record<string, unknown>[] {
    return this.crud.getItems('cliente');
  }

  ngOnInit(): void {
    // RF-1/RF-2/RF-3 necesitan viajes y clientes existentes para el formulario.
    if (this.viajes.length === 0) this.crud.loadList('viaje');
    if (this.clientes.length === 0) this.crud.loadList('cliente');
  }

  private validar(): boolean {
    this.viajeError = this.viajeId ? '' : 'Selecciona el viaje al que corresponde este gasto.';
    this.clienteError = this.clienteId ? '' : 'Selecciona el cliente responsable de pago.';
    const montoNum = Number(this.monto);
    this.montoError = this.monto && montoNum > 0 ? '' : 'Ingresa un monto mayor a S/ 0.00.';
    this.fechaError = this.fecha ? '' : 'Selecciona la fecha del gasto.';
    return !this.viajeError && !this.clienteError && !this.montoError && !this.fechaError;
  }

  save(): void {
    if (!this.validar()) return;

    this.saving.set(true);
    this.api
      .post<Gasto>('/gastos', {
        viaje_id: Number(this.viajeId),
        cliente_id: Number(this.clienteId),
        monto: Number(this.monto),
        fecha: this.fecha,
      })
      .pipe(timeout(HTTP_TIMEOUT_MS))
      .subscribe({
        next: () => {
          this.saving.set(false);
          this.toast.show('Gasto registrado correctamente. Ya puedes adjuntar el comprobante de pago.', '', 'ok');
          this.clearForm();
        },
        error: err => {
          this.saving.set(false);
          if (err instanceof HttpErrorResponse && err.status === 422) {
            this.viajeError = 'Este viaje no existe o no está disponible. Verifica el número de viaje.';
            return;
          }
          this.toast.show(mensajeError(err), '', 'err');
        },
      });
  }

  clearForm(): void {
    this.viajeId = '';
    this.clienteId = '';
    this.monto = '';
    this.fecha = new Date().toISOString().slice(0, 10);
    this.viajeError = '';
    this.clienteError = '';
    this.montoError = '';
    this.fechaError = '';
  }
}
