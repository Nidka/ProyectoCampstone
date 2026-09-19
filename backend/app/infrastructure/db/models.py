from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, CHAR, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UbigeoModel(Base):
    __tablename__ = "ubigeo"

    codigo_ubigeo: Mapped[int] = mapped_column(Integer, primary_key=True)
    provincia: Mapped[str] = mapped_column(String(25), nullable=False)
    distrito: Mapped[str] = mapped_column(String(25), nullable=False)
    departamento: Mapped[str] = mapped_column(String(25), nullable=False)
    estado_ubigeo: Mapped[bool] = mapped_column(Boolean, nullable=False)


class RubroModel(Base):
    __tablename__ = "rubro"

    id_rubro: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(100))
    estado_rubro: Mapped[bool] = mapped_column(Boolean, nullable=False)


class MarcaModel(Base):
    __tablename__ = "marca"

    id_marca: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    pais_origen: Mapped[Optional[str]] = mapped_column(String(100))
    fecha_fundacion: Mapped[Optional[date]] = mapped_column(Date)
    descripcion: Mapped[Optional[str]] = mapped_column(String(50))
    estado_marca: Mapped[bool] = mapped_column(Boolean, nullable=False)


class TipoUnidadModel(Base):
    __tablename__ = "tipounidad"

    id_tipo_unidad: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(50))
    estado_tipounidad: Mapped[bool] = mapped_column(Boolean, nullable=False)


class TipoGastoModel(Base):
    __tablename__ = "tipogasto"

    id_tipo_gasto: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(200))
    estado_tipogasto: Mapped[bool] = mapped_column(Boolean, nullable=False)


class ProductoCategoriaModel(Base):
    __tablename__ = "productocategoria"

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(200))
    estado_categoria: Mapped[bool] = mapped_column(Boolean, nullable=False)


class DireccionModel(Base):
    __tablename__ = "direccion"

    id_direccion: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo_ubigeo: Mapped[int] = mapped_column(ForeignKey("ubigeo.codigo_ubigeo"), nullable=False)
    direccion_detallada: Mapped[str] = mapped_column(String(200), nullable=False)
    referencia: Mapped[Optional[str]] = mapped_column(String(50))
    descripcion: Mapped[Optional[str]] = mapped_column(String(50))
    estado_direccion: Mapped[bool] = mapped_column(Boolean, nullable=False)


class SubtipoUnidadModel(Base):
    __tablename__ = "subtipounidad"

    id_subtipo_unidad: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_tipo_unidad: Mapped[int] = mapped_column(ForeignKey("tipounidad.id_tipo_unidad"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(50))
    estado_subtipounidad: Mapped[bool] = mapped_column(Boolean, nullable=False)


class ConductorModel(Base):
    __tablename__ = "conductor"

    id_conductor: Mapped[int] = mapped_column(Integer, primary_key=True)
    dni: Mapped[str] = mapped_column(CHAR(8), nullable=False, unique=True)
    nombre1: Mapped[str] = mapped_column(String(50), nullable=False)
    nombre2: Mapped[Optional[str]] = mapped_column(String(50))
    apellido1: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido2: Mapped[Optional[str]] = mapped_column(String(50))
    licencia_conducir: Mapped[str] = mapped_column(String(20), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    correo: Mapped[Optional[str]] = mapped_column(String(100))
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    fecha_nacimiento: Mapped[Optional[date]] = mapped_column(Date)
    estado_conductor: Mapped[bool] = mapped_column(Boolean, nullable=False)


class UnidadModel(Base):
    __tablename__ = "unidad"

    id_unidad: Mapped[int] = mapped_column(Integer, primary_key=True)
    placa: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    id_tipo_unidad: Mapped[int] = mapped_column(ForeignKey("tipounidad.id_tipo_unidad"), nullable=False)
    id_subtipo_unidad: Mapped[Optional[int]] = mapped_column(ForeignKey("subtipounidad.id_subtipo_unidad"))
    id_marca: Mapped[int] = mapped_column(ForeignKey("marca.id_marca"), nullable=False)
    modelo: Mapped[Optional[str]] = mapped_column(String(50))
    anio: Mapped[Optional[int]] = mapped_column(Integer)
    peso_tara: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    peso_maximo: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    estado_unidad: Mapped[bool] = mapped_column(Boolean, nullable=False)


class ClienteModel(Base):
    __tablename__ = "cliente"

    id_cliente: Mapped[int] = mapped_column(Integer, primary_key=True)
    razon_social: Mapped[str] = mapped_column(String(150), nullable=False)
    ruc: Mapped[str] = mapped_column(CHAR(11), nullable=False, unique=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    correo: Mapped[Optional[str]] = mapped_column(String(100))
    contacto: Mapped[Optional[str]] = mapped_column(String(100))
    id_rubro: Mapped[int] = mapped_column(ForeignKey("rubro.id_rubro"), nullable=False)
    id_direccion_domicilio: Mapped[Optional[int]] = mapped_column(ForeignKey("direccion.id_direccion"))
    estado_cliente: Mapped[bool] = mapped_column(Boolean, nullable=False)


class ConductorUnidadModel(Base):
    __tablename__ = "conductorunidad"

    id_conductor_unidad: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_conductor: Mapped[int] = mapped_column(ForeignKey("conductor.id_conductor"), nullable=False)
    id_unidad: Mapped[int] = mapped_column(ForeignKey("unidad.id_unidad"), nullable=False)
    fecha_asignacion: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_fin: Mapped[Optional[datetime]] = mapped_column(DateTime)
    estado_asignacion: Mapped[bool] = mapped_column(Boolean, nullable=False)


class ProgramacionViajeModel(Base):
    __tablename__ = "programacionviaje"

    id_viaje: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_tracto: Mapped[int] = mapped_column(ForeignKey("unidad.id_unidad"), nullable=False)
    id_carreta: Mapped[int] = mapped_column(ForeignKey("unidad.id_unidad"), nullable=False)
    id_conductor_unidad: Mapped[int] = mapped_column(ForeignKey("conductorunidad.id_conductor_unidad"), nullable=False)
    id_direccion_origen: Mapped[int] = mapped_column(ForeignKey("direccion.id_direccion"), nullable=False)
    id_direccion_destino: Mapped[int] = mapped_column(ForeignKey("direccion.id_direccion"), nullable=False)
    fecha_programado: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id_cliente"), nullable=False)
    estado_viaje: Mapped[bool] = mapped_column(Boolean, nullable=False)


class GuiaTransportistaModel(Base):
    __tablename__ = "guiatransportista"

    id_guia_transportista: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_guia: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    id_viaje: Mapped[int] = mapped_column(ForeignKey("programacionviaje.id_viaje"), nullable=False, unique=True)
    guias_remitente: Mapped[Optional[str]] = mapped_column(String(500))
    peso_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estado_guia: Mapped[bool] = mapped_column(Boolean, nullable=False)


class ViajeRealizadoModel(Base):
    __tablename__ = "viajerealizado"

    id_viaje_realizado: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_guia_transportista: Mapped[int] = mapped_column(
        ForeignKey("guiatransportista.id_guia_transportista"), nullable=False, unique=True
    )
    flete: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    fecha_llegada: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(String(200))
    estado_viaje_realizado: Mapped[bool] = mapped_column(Boolean, nullable=False)


class FacturaModel(Base):
    __tablename__ = "factura"

    id_factura: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_factura: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    id_viaje_realizado: Mapped[int] = mapped_column(ForeignKey("viajerealizado.id_viaje_realizado"), nullable=False, unique=True)
    monto_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estado_factura: Mapped[bool] = mapped_column(Boolean, nullable=False)


class PresupuestoViajeModel(Base):
    __tablename__ = "presupuestoviaje"

    id_presupuesto: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_viaje: Mapped[int] = mapped_column(ForeignKey("programacionviaje.id_viaje"), nullable=False, unique=True)
    monto_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    estado_presupuesto: Mapped[bool] = mapped_column(Boolean, nullable=False)


class DetallePresupuestoModel(Base):
    __tablename__ = "detallepresupuesto"

    id_detalle_presupuesto: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_presupuesto: Mapped[int] = mapped_column(ForeignKey("presupuestoviaje.id_presupuesto"), nullable=False)
    id_tipo_gasto: Mapped[int] = mapped_column(ForeignKey("tipogasto.id_tipo_gasto"), nullable=False)
    monto_estimado: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estado_detallepresupuesto: Mapped[Optional[bool]] = mapped_column(Boolean)


class ProductoTransportadoModel(Base):
    __tablename__ = "productotransportado"

    id_producto_transportado: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_guia_transportista: Mapped[int] = mapped_column(ForeignKey("guiatransportista.id_guia_transportista"), nullable=False)
    id_categoria: Mapped[int] = mapped_column(ForeignKey("productocategoria.id_categoria"), nullable=False)
    descripcion_producto: Mapped[str] = mapped_column(String(200), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estado_producto: Mapped[bool] = mapped_column(Boolean, nullable=False)


class UsuarioModel(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), nullable=False, default="operador")
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
