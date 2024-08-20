from fastapi import APIRouter

user_router = r = APIRouter()


@r.get("/self-profile")
async def self_profile(
):
    return {
        "full_name": "Python Developer",
        "user_name": f"pythonista"
    }
