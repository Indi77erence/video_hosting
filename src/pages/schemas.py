from pydantic import BaseModel


class GetSearchVideo(BaseModel):
	id: int
	title: str | None
	description: str | None
