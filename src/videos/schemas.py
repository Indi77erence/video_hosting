from typing import Union, Optional

from pydantic import BaseModel

from src.auth.models import User


class UploadVideo(BaseModel):
    title: str
    description: str | None = None


class UpdateVideo(BaseModel):
    title: str | None = None
    description: str | None = None



