from schemas.base import BaseUser


class UserRegisterIn(BaseUser):
    first_name: str
    last_name: str
    phone: str
    iban: str
    password: str


class UserLoginIn(BaseUser):
    password: str
