import { Component, inject } from '@angular/core';
import { ToastService } from '../../../core/services/toast.service';
import { Toast } from '../../../core/models/crud.model';

@Component({
  selector: 'app-toast',
  standalone: true,
  template: `
    <div class="toast-area">
      @for (t of toast.toasts(); track t.id) {
        <div class="toast {{ t.type }}">
          <div class="t-ic">{{ icons[t.type] }}</div>
          <div style="flex:1;min-width:0">
            <div class="t-title">{{ t.title }}</div>
            @if (t.msg) { <div class="t-msg">{{ t.msg }}</div> }
          </div>
          <button class="t-x" (click)="toast.remove(t.id)">×</button>
        </div>
      }
    </div>
  `,
})
export class ToastComponent {
  toast = inject(ToastService);
  icons: Record<string, string> = { ok:'✓', err:'✕', info:'i', warn:'!' };
}
