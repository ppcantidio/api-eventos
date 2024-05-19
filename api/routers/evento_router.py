from typing import List

from fastapi import APIRouter
from sqlmodel import Session

from api.db import engine
from api.models import Evento, EventoCreate, Usuario

router = APIRouter(prefix="/eventos")


@router.post("/", response_model=EventoCreate)
async def criar_evento(payload: EventoCreate):
    with Session(engine) as session:
        usuario = session.get(Usuario, payload.id_usuario)
        if usuario is None:
            return {"mensagem": "Usuário não encontrado"}
        evento = EventoCreate(**payload.model_dump())
        session.add(evento)
        session.commit()
        session.refresh(evento)
        return evento


@router.get("/{id}", response_model=Usuario)
async def get_evento(id: int):
    with Session(engine) as session:
        evento = session.get(Evento, id)
        if evento is None:
            return {"mensagem": "Evento não encontrado"}
        return evento


@router.get("/", response_model=List[Evento])
async def get_eventos():
    with Session(engine) as session:
        eventos = session.exec(Evento).all()
        return eventos


@router.put("/{id}", response_model=Evento)
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
