from pydantic import BaseModel


class GetComment(BaseModel):
	id: int
	content: str
	user_id: int
	video_id: int


class AddComment(BaseModel):
	id_video: int
	content: str


class UpdateComment(BaseModel):
	content: str | None = None
