from typing import Union

from pydantic import BaseModel


class CreateVideo(BaseModel):
	id: int
	title: str
	description: str
	file: str
	user: int


class UploadVideo(BaseModel):
	title: str
	description: str


class UpdateVideo(BaseModel):
	title: Union[str, None] = None
	description: Union[str, None] = None