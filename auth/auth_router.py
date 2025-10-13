from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Response, Cookie, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from data.db_core import get_session
import secrets

from models import User


router = APIRouter(prefix='/auth')

security = HTTPBasic()


def get_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                     db: get_session) -> User:
    correct_username = secrets.compare_digest(credentials.username)