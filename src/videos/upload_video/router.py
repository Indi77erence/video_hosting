from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from ..models import video as video_tbl
from .utils import save_video


router = APIRouter(
	prefix='/api/upload_video',
	tags=['Upload_video']
)


@router.post('')
async def upload_video(
		user_id: int,
		title: str = Form(...),
		description: str = Form(...),
		video: UploadFile = File(...),
		session: AsyncSession = Depends(get_async_session)
):
	path_video, info = await save_video(user_id, video, title, description)
	stmt = insert(video_tbl).values(file=path_video, user=user_id, **info.dict())
	await session.execute(stmt)
	await session.commit()
	return info
