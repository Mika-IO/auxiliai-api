from pydantic import BaseModel


class TokenRequest(BaseModel):
    email: str
    password: str


class Chat(BaseModel):
    name: str
    owner_id: str
