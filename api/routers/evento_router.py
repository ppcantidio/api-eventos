from typing import List

from fastapi import APIRouter
from sqlmodel import Session, select

from api.db import engine
from api.models import Evento, EventoCreate, Usuario, UsuarioEventosFavoritos

router = APIRouter(prefix="/eventos")


@router.post("/")
async def criar_evento(payload: EventoCreate):
    with Session(engine) as session:
        usuario = session.get(Usuario, payload.id_usuario)
        if usuario is None:
            return {"mensagem": "Usuário não encontrado"}
        evento = Evento(**payload.model_dump())
        session.add(evento)
        session.commit()
        session.refresh(evento)
        return evento


@router.get("/{id}")
async def get_evento(id: int):
    with Session(engine) as session:
        evento = session.get(Evento, id)
        if evento is None:
            return {"mensagem": "Evento não encontrado"}
        return evento


@router.get("/")
async def get_eventos():
    with Session(engine) as session:
        statement = select(Evento)
        eventos = session.exec(statement).all()
        return eventos


@router.put("/{id}")
async def editar_evento(id: int, payload: EventoCreate):
    with Session(engine) as session:
        evento = session.get(Evento, id)
        if evento is None:
            return {"mensagem": "Evento não encontrado"}
        evento.nome = payload.nome
        evento.descricao = payload.descricao
        evento.local = payload.local
        evento.data = payload.data
        session.add(evento)
        session.commit()
        session.refresh(evento)
        return evento


@router.delete("/{id}")
async def deletar_evento(id: int):
    with Session(engine) as session:
        evento = session.get(Evento, id)
        if evento is None:
            return {"mensagem": "Evento não encontrado"}
        session.delete(evento)
        session.commit()

        statement = select(UsuarioEventosFavoritos).where(
            UsuarioEventosFavoritos.id_evento == id
        )
        favoritos = session.exec(statement).all()
        for fav in favoritos:
            session.delete(fav)
            session.commit()
        return {"mensagem": "Evento deletado"}
