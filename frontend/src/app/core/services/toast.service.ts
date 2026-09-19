import { Injectable, signal } from '@angular/core';
import { Toast, ToastType } from '../models/crud.model';

@Injectable({ providedIn: 'root' })
export class ToastService {
  private _counter = 0;
  readonly toasts = signal<Toast[]>([]);

  show(title: string, msg = '', type: ToastType = 'info', dur = 4000): void {
    const id = ++this._counter;
    this.toasts.update(t => [...t, { id, title, msg, type }]);
    if (dur > 0) setTimeout(() => this.remove(id), dur);
  }

  remove(id: number): void {
    this.toasts.update(t => t.filter(x => x.id !== id));
  }
}
