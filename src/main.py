from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.auth.base_config import fastapi_users, auth_backend, current_user
from src.auth.schemas import UserRead, UserCreate

from .auth.models import User
from redis import asyncio as aioredis
from .upload_video.router import router as router_video
from .tasks.router import router as router_message_email


app = FastAPI(title='VideoHosting APP')

app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(router_message_email)
app.include_router(router_video)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_user)):
	return {"message": f"Hello {user.email}!"}


@app.on_event('startup')
async def startup_event():
	redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
	FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")