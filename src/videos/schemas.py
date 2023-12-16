from typing import Union

from pydantic import BaseModel


class UploadVideo(BaseModel):
	title: str
	description: str | None = None


class UpdateVideo(BaseModel):
	title: str | None = None
	description: str | None = None
