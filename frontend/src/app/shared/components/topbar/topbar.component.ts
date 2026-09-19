import { Component, inject, output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { CrudService } from '../../../core/services/crud.service';
import { ToastService } from '../../../core/services/toast.service';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.css'],
})
export class TopbarComponent {
  api   = inject(ApiService);
  crud  = inject(CrudService);
  toast = inject(ToastService);
  auth  = inject(AuthService);

  searchTerm = '';

  readonly back = output<void>();

  get health()   { return this.api.health(); }
  readonly usuario = this.auth.usuario;

  logout(): void { this.auth.logout(); }

  refresh(): void {
    this.crud.refreshAll();
    this.api.checkHealth();
  }

  onSearch(): void {
    // La búsqueda se maneja en cada CrudViewComponent vía input binding
  }
}
