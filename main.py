import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

logger = logging.getLogger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup: triggered")
    yield
    logger.info("shutdown: triggered")


def create_app() -> FastAPI:
    app = FastAPI()
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None)
