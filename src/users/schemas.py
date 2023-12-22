from pydantic import BaseModel


class GetDataUsers(BaseModel):
	id: int
	email: str
	username: str
	role_id: int
	is_verified: bool


class UpdateUser(BaseModel):
	email: str | None = None
	username: str | None = None


class DeleteUser(BaseModel):
	email: str
	username: str
