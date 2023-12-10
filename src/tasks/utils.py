import asyncio

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..upload_video.models import video as video_tbl

from src.database import get_async_session


async def async_get_last_video(session: AsyncSession = Depends(get_async_session)):
	stmt = select(video_tbl).order_by(video_tbl.c.title.desc()).limit(5)
	email_content = await session.execute(stmt)
	last_video = []
	for i in email_content.scalars():
		print(i)
		last_video.append(i)
	return last_video
