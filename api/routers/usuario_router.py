from fastapi import APIRouter
from sqlmodel import Session

from api.db import engine
from api.models import Usuario, UsuarioCreate

router = APIRouter(prefix="/usuarios")


@router.post("/", response_model=Usuario)
async def create_user(payload: UsuarioCreate):
    with Session(engine) as session:
        usuario = Usuario.model_validate(payload)
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario
