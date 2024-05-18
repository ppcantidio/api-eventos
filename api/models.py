import datetime
from typing import List

from sqlmodel import Field, Relationship, SQLModel


class UsuarioBase(SQLModel):
    nome: str
    email: str


class UsuarioCreate(UsuarioBase):
    senha: str


class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"
    id: int = Field(default=None, primary_key=True)
    eventos: List["Evento"] = Relationship(back_populates="usuario")


class Evento(SQLModel):
    id: int = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    local: str
    data: datetime
    usuario: Usuario = Relationship(back_populates="eventos")
