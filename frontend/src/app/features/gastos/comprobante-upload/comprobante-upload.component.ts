import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { timeout } from 'rxjs';
import { CrudService } from '../../../core/services/crud.service';
import { GastosApiService } from '../../../core/services/gastos-api.service';
import { ToastService } from '../../../core/services/toast.service';
import { Comprobante, Gasto } from '../../../core/models/gasto.model';
import { ESTADO_COMPROBANTE_CLASS, ESTADO_COMPROBANTE_LABEL, ESTADO_GASTO_CLASS, ESTADO_GASTO_LABEL } from '../../../core/models/gasto-estados';
import { HTTP_TIMEOUT_MS, mensajeError } from '../../../core/utils/error-messages';

const TIPOS_PERMITIDOS = ['image/png', 'image/jpeg', 'image/jpg', 'application/pdf'];
const TAMANO_MAXIMO = 10 * 1024 * 1024; // 10 MB

@Component({
  selector: 'app-comprobante-upload',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './comprobante-upload.component.html',
  styleUrls: ['./comprobante-upload.component.css'],
})
export class ComprobanteUploadComponent implements OnInit {
  private crud = inject(CrudService);
  private api = inject(GastosApiService);
  private toast = inject(ToastService);

  readonly estadoGastoLabel = ESTADO_GASTO_LABEL;
  readonly estadoGastoClass = ESTADO_GASTO_CLASS;
  readonly estadoComprobanteLabel = ESTADO_COMPROBANTE_LABEL;
  readonly estadoComprobanteClass = ESTADO_COMPROBANTE_CLASS;

  gastos = signal<Gasto[]>([]);
  comprobantes = signal<Comprobante[]>([]);
  gastoId = '';
  gastoError = '';
  selectedFile: File | null = null;
  fileError = '';
  isDragOver = signal(false);
  uploading = signal(false);

  // Getters normales (no signal computed()): dependen de gastoId, una
  // propiedad plana ligada por ngModel, no de una señal.
  get gastoSeleccionado(): Gasto | undefined {
    return this.gastos().find(g => String(g.id) === this.gastoId);
  }

  get comprobantesDelGasto(): Comprobante[] {
    const id = Number(this.gastoId);
    return this.comprobantes().filter(c => c.gasto_id === id);
  }

  ngOnInit(): void {
    if (this.crud.getItems('cliente').length === 0) this.crud.loadList('cliente');
    this.loadGastos();
    this.loadComprobantes();
  }

  loadGastos(): void {
    this.api.get<Gasto[]>('/gastos').pipe(timeout(HTTP_TIMEOUT_MS)).subscribe({
      next: rows => this.gastos.set(rows),
      error: err => this.toast.show(mensajeError(err), '', 'err'),
    });
  }

  loadComprobantes(): void {
    this.api.get<Comprobante[]>('/comprobantes').pipe(timeout(HTTP_TIMEOUT_MS)).subscribe({
      next: rows => this.comprobantes.set(rows),
      error: err => this.toast.show(mensajeError(err), '', 'err'),
    });
  }

  clienteNombre(clienteId: number): string {
    const cliente = this.crud.getItems('cliente').find((c: Record<string, unknown>) => c['id_cliente'] === clienteId);
    return (cliente?.['razon_social'] as string) ?? `Cliente #${clienteId}`;
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver.set(true);
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver.set(false);
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver.set(false);
    const file = event.dataTransfer?.files?.[0];
    if (file) this.handleFile(file);
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (file) this.handleFile(file);
    input.value = '';
  }

  private handleFile(file: File): void {
    if (!TIPOS_PERMITIDOS.includes(file.type)) {
      this.fileError = 'Solo se aceptan archivos JPG, PNG o PDF.';
      this.selectedFile = null;
      return;
    }
    if (file.size > TAMANO_MAXIMO) {
      this.fileError = 'El archivo supera el tamaño máximo permitido (10 MB).';
      this.selectedFile = null;
      return;
    }
    this.fileError = '';
    this.selectedFile = file;
  }

  subir(): void {
    this.gastoError = this.gastoId ? '' : 'Selecciona el gasto al que corresponde este comprobante.';
    if (!this.selectedFile) {
      this.fileError = 'Selecciona al menos un comprobante antes de continuar.';
    }
    if (this.gastoError || this.fileError || !this.selectedFile) return;

    this.uploading.set(true);
    this.api.uploadFile<Comprobante>(`/gastos/${this.gastoId}/comprobantes`, this.selectedFile).pipe(timeout(HTTP_TIMEOUT_MS)).subscribe({
      next: () => {
        this.uploading.set(false);
        this.toast.show('Comprobante adjuntado. El gasto cambió a estado "Pagado".', '', 'ok');
        this.selectedFile = null;
        this.loadGastos();
        this.loadComprobantes();
      },
      error: err => {
        this.uploading.set(false);
        if (err instanceof HttpErrorResponse && err.status === 422) {
          this.fileError = 'Solo se aceptan archivos JPG, PNG o PDF.';
          return;
        }
        this.toast.show(mensajeError(err), '', 'err');
      },
    });
  }

  fileUrl(archivoUrl: string): string {
    return this.api.fileUrl(archivoUrl);
  }
}
