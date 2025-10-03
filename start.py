from fastapi import FastAPI
from routers import routers

app = FastAPI()
for router in routers:
    app.include_router(router)

@app.get("/")
async def start():
    return {"status": "ok"}