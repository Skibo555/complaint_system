from typing import List

from fastapi import APIRouter, Depends, status
from starlette.requests import Request

from managers.auth import oauth2_schema, is_complainer, is_admin
from managers.complaint import ComplaintManager
from models import State
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut

router = APIRouter(tags=["Complaints"])


@router.get("/complaints", dependencies=[Depends(oauth2_schema)], response_model=List[ComplaintOut])
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplaintManager.get_complaints(user)


@router.post("/complaints", dependencies=[Depends(oauth2_schema), Depends(is_complainer)], response_model=ComplaintOut)
async def create_complaints(complaints: ComplaintIn, request: Request):
    user = request.state.user
    return await ComplaintManager.create_complaint(complaints.dict(), user)


@router.delete("/complaints/{complaint_id}", dependencies=[Depends(oauth2_schema), Depends(is_admin)],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_complaint(complaint_id: int):
    await ComplaintManager.delete(complaint_id)


@router.put("/complaints/{complaint_id}", dependencies=[Depends(oauth2_schema), Depends(is_admin)],
            status_code=status.HTTP_204_NO_CONTENT)
async def change_state(complaint_id: int, status: State):
    await ComplaintManager.approve_or_reject(complaint_id=complaint_id, state=status)
