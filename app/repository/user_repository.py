from sqlalchemy.ext.asyncio import AsyncSession
from utils.helpers.enums import Status
from schemas.base import User
from sqlalchemy.future import select

class UserRepository:
    async def create_user(self, user_data: dict, db : AsyncSession) -> User:
        new_user = User(
            username=user_data.get("username"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            email=user_data.get("email"),
            password_hash=user_data.get("password"),
        )
        
        if "email_verified" in user_data:
            new_user.email_verified = user_data["email_verified"]

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def get_user_by_email(self, email: str, db: AsyncSession) -> User:
        query = select(User).where(User.email == email, User.deleted_at == None)
        result = await db.execute(query)
        user = result.scalars().first()
        return user
    
    async def get_user_by_username(self, username: str, db: AsyncSession) -> User:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        user = result.scalars().first()
        return user
    
    async def get_user_by_user_id(self, user_id: int, db: AsyncSession) -> User:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalars().first()
        return user
    
    async def update_user_email_verification(self, user: User, db: AsyncSession):
        user.email_verified = True
        await db.commit()
        await db.refresh(user)
    
    async def update_user_status_to_active(self, user: User, db: AsyncSession):
        user.status = Status.ACTIVE.value
        await db.commit()
        await db.refresh(user)
    


