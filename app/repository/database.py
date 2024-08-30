from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from config import get_config


DATABASE_URL = get_config().database_url

async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e

async def check_database_connection():
    try:
        async with async_engine.connect() as conn:
            async with conn.begin():  
                def sync_inspect(conn: AsyncConnection):
                    inspector = inspect(conn)
                    tables = inspector.get_table_names()
                    return tables
                
                tables = await conn.run_sync(sync_inspect)

            print("Tables in the database:")
            for table in tables:
                print(table)
        print("Database connection successful!")
    except OperationalError:
        print("Database connection failed!")
        raise 