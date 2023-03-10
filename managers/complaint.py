from models import complaint
from models import RoleType, State
from db import database


class ComplaintManager:

    @staticmethod
    async def get_complaints(user):
        q = complaint.select()
        if user["role"] == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            q = q.where(complaint.c.state == State.pending)
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data["complainer_id"] = user["id"]
        id_ = await database.execute(complaint.insert().values(complaint_data))
        # complain data . dict ()
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def reject(complaint_id):
        await database.execute(complaint.update().where(complaint.c.id == complaint_id).values(status=State.rejected))

    @staticmethod
    async def approve(complaint_id):
        await database.execute(complaint.update().where(complaint.c.id == complaint_id).values(status=State.approved))
