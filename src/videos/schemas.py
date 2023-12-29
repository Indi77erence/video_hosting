from pydantic import BaseModel


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


class UploadVideo(BaseModel):
    title: str
    description: str | None = None


class UpdateVideo(BaseModel):
    title: str | None = None
    description: str | None = None


class PlayVideo(BaseModel):
    title: str


