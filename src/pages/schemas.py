from pydantic import BaseModel

from src.auth.schemas import GetAllUsers


class GetSearchVideo(BaseModel):
	id: int
	title: str | None
	description: str | None
	user_id: int


class GetSearchVideoUser(BaseModel):
	id: int
	title: str | None
	description: str | None
	user_id: int
