from pydantic import BaseModel


class GetSearchVideo(BaseModel):
	title: str
	description: str
