import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap } from 'rxjs';
import { LoginRequest, RegisterRequest, TokenResponse, UsuarioOut } from '../models/auth.model';
import { ApiService } from './api.service';

const TOKEN_KEY = 'lizar_token';
const USER_KEY  = 'lizar_user';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private _token   = signal<string | null>(localStorage.getItem(TOKEN_KEY));
  private _usuario = signal<UsuarioOut | null>(
    JSON.parse(localStorage.getItem(USER_KEY) ?? 'null')
  );

  readonly token   = this._token.asReadonly();
  readonly usuario = this._usuario.asReadonly();
  readonly isAuth  = computed(() => !!this._token());
  readonly isAdmin = computed(() => this._usuario()?.rol === 'admin');

  constructor(private http: HttpClient, private router: Router, private api: ApiService) {}

  login(body: LoginRequest) {
    return this.http
      .post<TokenResponse>(`${this.api.base()}/auth/login`, body)
      .pipe(
        tap(res => {
          this._token.set(res.access_token);
          this._usuario.set(res.usuario);
          localStorage.setItem(TOKEN_KEY, res.access_token);
          localStorage.setItem(USER_KEY, JSON.stringify(res.usuario));
        })
      );
  }

  register(body: RegisterRequest) {
    return this.http.post<UsuarioOut>(`${this.api.base()}/auth/register`, body);
  }

  logout(): void {
    this._token.set(null);
    this._usuario.set(null);
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    this.router.navigate(['/login']);
  }
}
