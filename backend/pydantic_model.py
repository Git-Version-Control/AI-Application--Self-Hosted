from pydantic import BaseModel

class UserDetail(BaseModel):
    user_id: int
    email: str