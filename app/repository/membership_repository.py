from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.base import Membership

class MembershipRepository:
    async def get_membership_by_user_id_and_role(self, user_id: int, role: str, db: AsyncSession) -> Membership:
        query = select(Membership).where(Membership.user_id == user_id, Membership.role == role)
        result = await db.execute(query)
        return result.scalars().first()

    async def create_membership(self, user_id: int, organization_id: int, role: str, db: AsyncSession) -> Membership:
        new_membership = Membership(user_id=user_id, organization_id=organization_id, role=role)
        db.add(new_membership)
        await db.commit()
        await db.refresh(new_membership)
        return new_membership
