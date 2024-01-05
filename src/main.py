import time
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from starlette.staticfiles import StaticFiles
from src.auth.base_config import fastapi_users, auth_backend

from redis import asyncio as aioredis

from .auth.schemas import UserRead, UserCreate
from .videos.router import router as video_router
from .users.router import router as user_router
from .comment.router import router as comment_router
from .back_tasks.router import router as router_message_email
from .pages.router import router as pages_router


app = FastAPI(title='VideoHosting APP')

app.mount("/static", StaticFiles(directory="src/videos/users_video/static"), name="static")
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"])


app.include_router(user_router)
app.include_router(video_router)
app.include_router(comment_router)
app.include_router(router_message_email)
app.include_router(pages_router)


@app.on_event('startup')
async def startup_event():
	redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
	FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get('/test/any_long_operation')
@cache(expire=3600)
def get_long_op():
	time.sleep(3)
	return 'Много-много данных!'




