from fastapi import APIRouter
from sqlalchemy.orm import joinedload
from sqlmodel import Session

from api.db import engine
from api.models import Usuario, UsuarioCreate

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
