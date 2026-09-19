from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.auth.application.schemas import LoginRequest, RegisterRequest, TokenResponse, UsuarioOut
from app.features.auth.application.use_cases import ALGORITHM, SECRET_KEY, LoginUseCase, RegisterUseCase
from app.features.auth.infrastructure.sql_repository import SqlUsuarioRepository
from app.infrastructure.db.models import UsuarioModel
from app.shared.exceptions import ConflictError, NotFoundError

router = APIRouter(prefix="/auth", tags=["auth"])


def get_repo(db: Session = Depends(get_db_session)) -> SqlUsuarioRepository:
    return SqlUsuarioRepository(db)


def get_current_user(
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db_session),
) -> UsuarioModel:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user = SqlUsuarioRepository(db).get_by_username(username)
    if not user or not user.estado:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, repo: SqlUsuarioRepository = Depends(get_repo)):
    try:
        return LoginUseCase(repo).execute(body.username, body.password)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/register", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, repo: SqlUsuarioRepository = Depends(get_repo)):
    try:
        return RegisterUseCase(repo).execute(
            body.username, body.email, body.password, body.nombre, body.rol
        )
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/me", response_model=UsuarioOut)
def me(current_user: UsuarioModel = Depends(get_current_user)):
    return current_user
