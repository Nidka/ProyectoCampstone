export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  nombre: string;
  rol: 'admin' | 'operador';
}

export interface UsuarioOut {
  id_usuario: number;
  username: string;
  email: string;
  nombre: string;
  rol: 'admin' | 'operador';
  estado: boolean;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  usuario: UsuarioOut;
}
