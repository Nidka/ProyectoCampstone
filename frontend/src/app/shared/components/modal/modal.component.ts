import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-modal',
  standalone: true,
  template: `
    @if (visible()) {
      <div class="mbg on" (click)="close()">
        <div class="modal" (click)="$event.stopPropagation()">
          <div class="m-hd">
            <h3>{{ title() }}</h3>
            <button class="btn btn-ghost btn-sm" (click)="close()">✕ Cerrar</button>
          </div>
          <div class="m-bd"><pre>{{ body() }}</pre></div>
        </div>
      </div>
    }
  `,
})
export class ModalComponent {
  visible = signal(false);
  title   = signal('');
  body    = signal('');

  show(title: string, data: unknown): void {
    this.title.set(title);
    this.body.set(typeof data === 'string' ? data : JSON.stringify(data, null, 2));
    this.visible.set(true);
  }

  close(): void { this.visible.set(false); }
}
