import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.db import create_db_and_tables
from api.routers import evento_router

logger = logging.getLogger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup: triggered")
    create_db_and_tables()
    yield
    logger.info("shutdown: triggered")


def add_routers(app: FastAPI):
    from api.routers import usuario_router

    app.include_router(usuario_router.router)
    app.include_router(evento_router.router)


def add_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    add_routers(app)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
