from typing import List

from fastapi import APIRouter
from sqlalchemy.orm import joinedload
from sqlmodel import Session

from api.db import engine
from api.models import (
    Evento,
    FavoritarEvento,
    Usuario,
    UsuarioCreate,
    UsuarioEventosFavoritos,
    UsuarioLogin,
)

router = APIRouter(prefix="/usuarios")


@router.post("/", response_model=Usuario)
async def criar_usuario(payload: UsuarioCreate):
    with Session(engine) as session:
        usuario = Usuario.model_validate(payload)
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario


@router.get("/{id}", response_model=Usuario)
async def get_usuario(id: int):
    with Session(engine) as session:
        usuario = (
            session.exec(Usuario)
            .options(joinedload(Usuario.eventos))
            .filter(Usuario.id == id)
            .first()
        )
        return usuario


@router.post("/login")
async def login(payload: UsuarioLogin):
    with Session(engine) as session:
        usuario = session.exec(Usuario).filter(Usuario.email == payload.email).first()
        if not usuario:
            return {"mensagem": "Usuário não encontrado"}
        if usuario.senha != payload.senha:
            return {"mensagem": "Senha incorreta"}
        return usuario


@router.post("/{id_usuario}/favoritar")
async def favoritar_evento(payload: FavoritarEvento, id_usuario: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id_usuario)
        if usuario is None:
            return {"mensagem": "Usuário não encontrado"}
        evento = session.get(Evento, payload.id_evento)
        if evento is None:
            return {"mensagem": "Evento não encontrado"}
        usuario.eventos_favoritos.append(evento)
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario


@router.get("/{id_usuario}/eventos_favoritos", response_model=List[Evento])
async def get_eventos_favoritos(id_usuario: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id_usuario)
        if usuario is None:
            return {"mensagem": "Usuário não encontrado"}
        return usuario.eventos_favoritos


@router.delete("/{id_usuario}/eventos_favoritos/{id_evento}")
async def deletar_evento_favorito(id_usuario: int, id_evento: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id_usuario)
        if usuario is None:
            return {"mensagem": "Usuário não encontrado"}
        evento_favorito = session.get(UsuarioEventosFavoritos, id_evento)
        if evento_favorito is None:
            return {"mensagem": "Evento não encontrado"}
        session.delete(evento_favorito)
        session.commit()
        return {"mensagem": "Evento removido dos favoritos"}
