from fastapi import APIRouter
from sqlalchemy.orm import joinedload
from sqlmodel import Session

from api.db import engine
from api.models import Usuario, UsuarioCreate, UsuarioLogin

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
