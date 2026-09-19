import { Injectable, signal } from '@angular/core';
import { ApiService } from './api.service';
import { ToastService } from './toast.service';
import { CrudDef } from '../models/crud.model';
import { CRUDS } from '../models/cruds.data';
import { catchError, of } from 'rxjs';

type RecordMap = Record<string, unknown>;

@Injectable({ providedIn: 'root' })
export class CrudService {
  /** Cache local de todos los módulos */
  readonly data = signal<Record<string, RecordMap[]>>({});

  readonly cruds: CrudDef[] = CRUDS;

  constructor(private api: ApiService, private toast: ToastService) {}

  getCrud(key: string): CrudDef | undefined {
    return this.cruds.find(c => c.key === key);
  }

  getItems(key: string): RecordMap[] {
    return this.data()[key] ?? [];
  }

  /** Carga una lista desde la API */
  loadList(key: string): void {
    const c = this.getCrud(key);
    if (!c) return;
    this.api.get<RecordMap[] | { items?: RecordMap[]; data?: RecordMap[] }>(c.route).pipe(
      catchError(err => { this.toast.show('Sin conexión', err.message, 'err'); return of([]); })
    ).subscribe(res => {
      const items: RecordMap[] = Array.isArray(res) ? res : (res as any)?.items ?? (res as any)?.data ?? [];
      this.data.update(d => ({ ...d, [key]: items }));
    });
  }

  /** Guarda un nuevo registro */
  saveItem(key: string, payload: RecordMap): void {
    const c = this.getCrud(key);
    if (!c) return;
    this.api.post<RecordMap>(c.route, payload).pipe(
      catchError(err => {
        const msg = err?.error?.detail ?? err.message ?? 'Error';
        this.toast.show(`No se pudo guardar`, Array.isArray(msg) ? msg.map((e: any) => e.msg).join(' · ') : msg, 'err');
        return of(null);
      })
    ).subscribe(res => {
      if (!res) return;
      this.toast.show(`${c.title} guardado`, 'Registro creado correctamente', 'ok');
      this.loadList(key);
    });
  }

  /** Refresca todos los módulos */
  refreshAll(): void {
    this.cruds.forEach(c => this.loadList(c.key));
    this.toast.show('Datos actualizados', '', 'ok', 2200);
  }
}
