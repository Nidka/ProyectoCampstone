import { Injectable, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

/** Rol simulado mientras no exista Gestión de Usuarios (RF-19 a RF-21). */
export type RolSimulado = 'operador' | 'logistica';

@Injectable({ providedIn: 'root' })
export class GastosApiService {
  private readonly storageKey = 'lizar_gastos_api_base';
  private readonly defaultBase = 'http://localhost:8081';
  private _base = signal(localStorage.getItem(this.storageKey) ?? this.defaultBase);
  readonly base = this._base.asReadonly();

  /** Usuario/rol actual simulado por header (RF-7). */
  readonly currentUser = signal<{ nombre: string; rol: RolSimulado }>({
    nombre: 'Ana Torres',
    rol: 'operador',
  });

  constructor(private http: HttpClient) {}

  setBase(url: string): void {
    const normalized = url.trim().replace(/\/$/, '');
    this._base.set(normalized);
    localStorage.setItem(this.storageKey, normalized);
  }

  private headers(): HttpHeaders {
    const u = this.currentUser();
    return new HttpHeaders({ 'X-User-Name': u.nombre, 'X-User-Role': u.rol });
  }

  get<T>(path: string): Observable<T> {
    return this.http.get<T>(`${this._base()}${path}`, { headers: this.headers() });
  }

  post<T>(path: string, body: unknown): Observable<T> {
    return this.http.post<T>(`${this._base()}${path}`, body, { headers: this.headers() });
  }

  uploadFile<T>(path: string, file: File): Observable<T> {
    const form = new FormData();
    form.append('archivo', file);
    return this.http.post<T>(`${this._base()}${path}`, form, { headers: this.headers() });
  }

  fileUrl(archivoUrl: string): string {
    return archivoUrl.startsWith('http') ? archivoUrl : `${this._base()}${archivoUrl}`;
  }
}
