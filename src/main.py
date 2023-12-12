from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.staticfiles import StaticFiles

from src.auth.base_config import fastapi_users, auth_backend, current_user
from src.auth.schemas import UserRead, UserCreate
from .auth.models import User
from redis import asyncio as aioredis
from .videos.get_info_video.router import router as get_info_video_router
from .videos.upload_video.router import router as upload_video_router
from .videos.play_video.router import router as play_video_router
from .tasks.router import router as router_message_email
from .pages.router import router as router_pages

app = FastAPI(title='VideoHosting APP')

app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])

app.include_router(router_message_email)

app.include_router(get_info_video_router)
app.include_router(upload_video_router)
app.include_router(play_video_router)
app.include_router(router_pages)


@app.on_event('startup')
async def startup_event():
	redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
	FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_user)):
	return {"message": f"Hello {user.email}!"}


