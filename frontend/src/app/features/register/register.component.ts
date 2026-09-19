import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrls: ['../login/login.component.css', './register.component.css'],
})
export class RegisterComponent {
  private auth = inject(AuthService);
  private router = inject(Router);

  username = '';
  email = '';
  nombre = '';
  rol: 'admin' | 'operador' = 'operador';
  password = '';
  confirmPassword = '';

  loading = signal(false);
  error = signal('');
  showPass = signal(false);

  submit(): void {
    if (!this.username.trim() || !this.email.trim() || !this.nombre.trim() || !this.password) {
      this.error.set('Completa todos los campos obligatorios');
      return;
    }
    if (this.password.length < 6) {
      this.error.set('La contraseña debe tener al menos 6 caracteres');
      return;
    }
    if (this.password !== this.confirmPassword) {
      this.error.set('Las contraseñas no coinciden');
      return;
    }

    this.error.set('');
    this.loading.set(true);
    this.auth.register({
      username: this.username.trim(),
      email: this.email.trim(),
      nombre: this.nombre.trim(),
      rol: this.rol,
      password: this.password,
    }).subscribe({
      next: () => this.router.navigate(['/login'], { queryParams: { registered: '1' } }),
      error: (e) => {
        this.error.set(e?.error?.detail ?? 'No se pudo crear el usuario');
        this.loading.set(false);
      },
    });
  }
}
