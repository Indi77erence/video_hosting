from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from ..models import video as video_tbl
from .utils import save_video
from ...auth.base_config import current_user

router = APIRouter(
	prefix='/api',
	tags=['Upload_video']
)


@router.post('/upload_video')
async def upload_video(
		user=Depends(current_user),
		title: str = Form(...),
		description: str = None,
		video: UploadFile = File(...),
		session: AsyncSession = Depends(get_async_session),
):
	path_video, info = await save_video(user.id, video, title, description)
	stmt = insert(video_tbl).values(file=path_video, user=user.id, **info.dict())
	await session.execute(stmt)
	await session.commit()
	return info
