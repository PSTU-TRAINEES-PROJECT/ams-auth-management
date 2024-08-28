import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import const, auth
from config import get_config
from routers.api.v1 import user_router


app = FastAPI(
    title=get_config().project_title,
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware, allow_headers=["*"], allow_origins=["*"], allow_methods=["*"]
)

app.include_router(
    user_router,
    prefix=const.API_STR,
    tags=["users_management"]
)


# Register the events
# app.add_event_handler("startup", auth.on_startup)
# app.add_event_handler("shutdown", auth.on_shutdown)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=get_config().is_reload,
        port=get_config().backend_port,
    )
