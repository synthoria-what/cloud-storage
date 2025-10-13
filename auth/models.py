from pydantic import BaseModel, Field



class User(BaseModel):
    username: str = Field(description="Логин пользователя")
    password: str = Field(description="Пароль пользователя")
    email: str = Field(default=None, description="Почта пользователя")
    role: str = Field(default="user", description="Роль пользователя")