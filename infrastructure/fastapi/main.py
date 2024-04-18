"""Bismillahirrahmanirrahim"""
import sys
import os
from contextlib import asynccontextmanager

ROOT_DIR = os.getcwd()
sys.path.append(ROOT_DIR)

import uvicorn
from fastapi import FastAPI, Request

from api.rest.v0.controllers import app as v0_app
from api.gql.app import app as gql_app

from infrastructure.asyncpg import Database
from config import APP_CONFIG


db = Database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on app startup
    await db.create_pool()
    yield
    # on app shutdown

app = FastAPI(
    **APP_CONFIG,
    lifespan=lifespan,
)
app.mount("/api/v0", v0_app)
app.mount("/api", gql_app)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.pgpool = db.pool
    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, workers=1)
