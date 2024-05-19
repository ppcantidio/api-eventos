import stat
from typing import List

from fastapi import APIRouter, Response
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select
from starlette.responses import JSONResponse

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


@router.post("/")
async def criar_usuario(payload: UsuarioCreate):
    with Session(engine) as session:
        statement = select(Usuario).where(Usuario.email == payload.email)
        result = session.exec(statement)
        usuario_ja_existe = result.one_or_none()
        if usuario_ja_existe is None:
            usuario = Usuario(**payload.model_dump())
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            return usuario
        return Response(
            status_code=400, content=JSONResponse({"message": "Usuário já existe"})
        )


@router.get("/{id}")
async def get_usuario(id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id)
        if usuario is None:
            return Response(status_code=204)
        response = usuario.model_dump()
        response["eventos"] = usuario.eventos
        response["eventos_favoritos"] = [
            fav.evento for fav in usuario.eventos_favoritos
        ]
        return response


@router.post("/login")
async def login(payload: UsuarioLogin):
    with Session(engine) as session:
        statement = select(Usuario).where(Usuario.email == payload.email)
        result = session.exec(statement)
        usuario = result.one_or_none()
        if not usuario:
            return Response(status_code=204)
        if usuario.senha != payload.senha:
            return Response(status_code=204)
        return usuario


@router.post("/{id_usuario}/favoritar")
async def favoritar_evento(payload: FavoritarEvento, id_usuario: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id_usuario)
        if usuario is None:
            return Response(status_code=204)
        evento = session.get(Evento, payload.id_evento)
        if evento is None:
            return Response(status_code=204)

        evento_favorito = UsuarioEventosFavoritos(
            id_usuario=id_usuario, id_evento=payload.id_evento
        )
        session.add(evento_favorito)
        session.commit()
        session.refresh(evento_favorito)
        response = usuario.model_dump()
        response["eventos"] = usuario.eventos
        response["eventos_favoritos"] = [
            fav.evento for fav in usuario.eventos_favoritos
        ]
        return response


@router.get("/{id_usuario}/eventos_favoritos")
async def get_eventos_favoritos(id_usuario: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id_usuario)
        if usuario is None:
            return Response(status_code=204)
        return usuario.eventos_favoritos


@router.delete("/{id_usuario}/eventos_favoritos/{id_evento}")
async def deletar_evento_favorito(id_usuario: int, id_evento: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id_usuario)
        if usuario is None:
            return Response(status_code=204)
        evento_favorito = session.get(UsuarioEventosFavoritos, id_evento)
        if evento_favorito is None:
            return Response(status_code=204)
        session.delete(evento_favorito)
        session.commit()
        return {"mensagem": "Evento removido dos favoritos"}
