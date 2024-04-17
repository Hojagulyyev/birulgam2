"""Bismillahirrahmanirrahim"""
import sys
import os
from contextlib import asynccontextmanager

ROOT_DIR = os.getcwd()
sys.path.append(ROOT_DIR)

import uvicorn
from fastapi import FastAPI

from api.rest.v0.controllers import app as v0_app
from api.gql.app import app as gql_app

from infrastructure.asyncpg import get_pool
from config import APP_CONFIG


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on app startup
    global pool
    pool = await get_pool()
    yield
    # on app shutdown
    await pool.close()


app = FastAPI(
    **APP_CONFIG,
    lifespan=lifespan,
)
app.mount("/api/v0", v0_app)
app.mount("/api", gql_app)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, workers=1)
