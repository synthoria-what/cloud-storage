from fastapi import FastAPI

from auth.auth_router import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def start():
    return {"status": "ok"}