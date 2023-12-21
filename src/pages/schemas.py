from pydantic import BaseModel

from src.auth.schemas import GetAllUsers


class GetSearchVideo(BaseModel):
	id: int | None
	title: str | None
	description: str | None
	user: int | None


class GetSearchVideoUser(BaseModel):
	id: int
	title: str | None
	description: str | None
	user: int


