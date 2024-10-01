from db import database
from models import complaint, State, user
from models.enums import RoleType


class ComplaintManager:

    @staticmethod
    async def get_complaints(user):
        q = complaint.select()
        if user["role"] == RoleType.complainer:
            result = q.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.admin:
            result = q.where(complaint.c.status == State.pending)
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complain_data, user_id):
        complain_data["complainer_id"] = user_id["id"]
        result = await database.execute(complaint.insert().values(complain_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == result))

    @staticmethod
    async def delete(complaint_id):
        q = await database.execute(complaint.delete().where(complaint.c.id == complaint_id))
        return q

    @staticmethod
    async def approve_or_reject(complaint_id, state: State):
        await database.execute(complaint.update().where(complaint.c.id == complaint_id).values(status=state))
