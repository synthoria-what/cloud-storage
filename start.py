from fastapi import FastAPI
from routers import routers
from data.models.users import User
from data.db_core import init_db
from contextlib import asynccontextmanager
import asyncio



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Бд инициализируется")
    await init_db()
    yield
    print("Бд закрыта")

app = FastAPI(lifespan=lifespan)
for router in routers:
    app.include_router(router)


@app.get("/")
async def start():
    return {"status": "ok"} 