from pydantic import BaseModel

class UserMo(BaseModel):
    id: str | None = None
    username: str
    email: str