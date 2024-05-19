from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class UsuarioLogin(SQLModel):
    email: str
    senha: str


class UsuarioBase(SQLModel):
    nome: str
    email: str


class UsuarioCreate(UsuarioBase):
    senha: str


class FavoritarEvento(BaseModel):
    id_evento: int


class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"
    id: int = Field(default=None, primary_key=True)
    eventos: List["Evento"] = Relationship(back_populates="usuario")
    eventos_favoritos: List["UsuarioEventosFavoritos"] = Relationship(
        back_populates="usuario"
    )


class EventoBase(SQLModel):
    id_usuario: int = Field(default=None, foreign_key="usuarios.id")
    nome: str
    descricao: str
    local: str
    data: datetime


class EventoCreate(EventoBase):
    pass


class Evento(EventoBase):
    id: int = Field(default=None, primary_key=True)
    usuario: Usuario = Relationship(back_populates="eventos")


class UsuarioEventosFavoritos(SQLModel):
    id_usuario: int = Field(default=None, foreign_key="usuarios.id")
    id_evento: int = Field(default=None, foreign_key="eventos.id")
    usuario: Usuario = Relationship(back_populates="eventos_favoritos")
