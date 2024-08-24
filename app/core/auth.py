from repository.database import check_database_connection


async def on_startup():
    await check_database_connection()
    print("Application startup: Database connection checked.")

async def on_shutdown():
    print("Application shutdown: Cleaning up resources.")

