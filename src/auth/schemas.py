from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel


class UserCreate(schemas.BaseUserCreate):
	username: str
	email: str
	password: str
	role_id: Optional[int] = 2
	is_active: Optional[bool] = True
	is_superuser: Optional[bool] = False
	is_verified: Optional[bool] = False


class UserRead(schemas.BaseUser[int]):
	id: int | None
	email: str | None
	username: str | None
	role_id: int | None
	is_active: bool = True
	is_superuser: bool = False
	is_verified: bool = False

	class Config:
		orm_mode = True


class UserUpdate(schemas.BaseUser[int]):
	email: str
	username: str

	class Config:
		orm_mode = True


class Video(BaseModel):
	id: int
	title: str | None
	description: str | None


class GetAllUsers(BaseModel):
	id: int
	email: str
	username: str


class MyUserCreate(schemas.BaseUserCreate):
	id: int
	username: str
	email: str
	password: str
	role_id: int
	is_active: Optional[bool] = True
	is_superuser: Optional[bool] = False
	is_verified: Optional[bool] = False

