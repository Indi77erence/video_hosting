from pydantic import BaseModel


class GetSearchVideo(BaseModel):
	id: int
	title: str
	description: str
