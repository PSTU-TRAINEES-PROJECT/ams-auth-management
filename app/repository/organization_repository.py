from sqlalchemy.ext.asyncio import AsyncSession
from schemas.base import Organization
from sqlalchemy.future import select

class OrganizationRepository:
    async def create_organization(self, name: str, db: AsyncSession) -> Organization:
        new_organization = Organization(name=name)
        db.add(new_organization)
        await db.commit()
        await db.refresh(new_organization)
        return new_organization

    async def get_organization_by_name(self, name: str, db: AsyncSession) -> Organization:
        query = select(Organization).where(Organization.name == name)
        result = await db.execute(query)
        return result.scalars().first()


