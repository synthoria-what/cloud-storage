from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Response, Cookie, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from data.db_core import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets

from data.models.users import User
from .models import User as pydantic_User


router = APIRouter(prefix='/auth')

security = HTTPBasic()


async def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_session)]
) -> User:
    stmt = select(User).where(User.username == credentials.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    correct_username = secrets.compare_digest(credentials.username, user.username)
    correct_password = secrets.compare_digest(credentials.password, user.passw)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return user




@router.get("/profile")
async def get_profile(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "username": current_user.username,
        "password": current_user.passw,
        "role": current_user.role
    }
    
    
@router.post("/register")
async def register(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_session)]):
    stmt = select(User).where(User.username == credentials.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        return {"result": "Пользователь уже существует"}
    new_user = User(username=credentials.username, passw=credentials.password)
    db.add(new_user)
    return {"status": "ok", "data": {"message": "Пользователь был успешно добавлен"}}