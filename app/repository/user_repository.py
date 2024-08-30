from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import User
from sqlalchemy.future import select

class UserRepository:
    async def save_user(self, user_data: dict, db : AsyncSession) -> dict:
        new_user = User(
            username=user_data.get("username"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            email=user_data.get("email"),
            password_hash=user_data.get("password"),
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {"id": new_user.id, "email": new_user.email}

    async def get_user_by_email(self, email: str, db: AsyncSession) -> dict:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        user = result.scalars().first()
        return user
    
    async def get_user_by_username(self, username: str, db: AsyncSession) -> dict:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        user = result.scalars().first()
        return user
    
    async def get_all_users(self, db: AsyncSession) -> list[User]:
        query = select(User)
        result = await db.execute(query)
        users = result.scalars().all()
        return users


