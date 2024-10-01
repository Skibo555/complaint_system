from typing import Optional, List

from fastapi import APIRouter, Depends, status

from managers.auth import oauth2_schema, is_admin
from managers.user import UserManager
from models import RoleType
from schemas.response.user import UserOut

router = APIRouter(tags=["User"])


@router.get("/users/", dependencies=[Depends(oauth2_schema), Depends(is_admin)],
            response_model=List[UserOut])
async def get_all_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()


@router.put("/users/{user_id}", dependencies=[Depends(oauth2_schema), Depends(is_admin)], status_code=status.HTTP_204_NO_CONTENT)
async def change_role(user_id: int, role: RoleType):
    await UserManager.change_role(role=role, user_id=user_id)


