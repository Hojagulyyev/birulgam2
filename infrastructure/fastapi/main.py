"""Bismillahirrahmanirrahim"""
import sys
import os

ROOT_DIR = os.getcwd()
sys.path.append(ROOT_DIR)

import uvicorn
from fastapi import FastAPI

from api.rest.v0.controllers import app as v0_app
from api.gql.app import app as gql_app

from config import APP_CONFIG

 

app = FastAPI(**APP_CONFIG)
app.mount("/api/v0", v0_app)
app.mount("/api", gql_app)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, workers=1)
