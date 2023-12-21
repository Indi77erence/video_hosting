from pydantic import BaseModel


class UpdateUser(BaseModel):
    email: str | None = None
    username: str | None = None