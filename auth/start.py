from fastapi import FastAPI
from contextlib import asynccontextmanager

from auth_router import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def start():
    return {"status": "ok"}