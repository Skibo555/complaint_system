from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr


class ComplaintBase(BaseModel):
    title: str
    description: str
    photo_url: str
    amount: float
    # complainer_id: int
