from fastapi import HTTPException, status
from passlib.context import CryptContext

from db import database
from models.users import user
from models.enums import RoleType
from asyncpg import UniqueViolationError

from managers.auth import AuthManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register_user(user_info):
        user_info["password"] = pwd_context.hash(user_info["password"])
        # print(f"From the register function top {user.json()}")
        try:
            user_id = await database.execute(user.insert().values(**user_info))
            print(user_id)
        except UniqueViolationError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        new_user = await database.fetch_one(user.select().where(user.c.id == user_id))

        return AuthManager.encode_token(new_user)

    @staticmethod
    async def login(user_info):
        check_user = await database.fetch_one(user.select().where(user.c.email == user_info["email"]))
        if not check_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password or email.")
        if not pwd_context.verify(user_info["password"], check_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password or email.")
        return AuthManager.encode_token(check_user)

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(user.select())

    @staticmethod
    async def get_user_by_email(email):
        return await database.fetch_one(user.select().where(user.c.email == email))

    @staticmethod
    async def change_role(role: RoleType, user_id):
        await database.execute(user.update().where(user.c.id == user_id).values(role=role))


