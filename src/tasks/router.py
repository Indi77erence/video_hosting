from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..upload_video.models import video as video_tbl
from .tasks import send_email_report_last_video
from ..auth.base_config import current_user


router = APIRouter(prefix="/report")


@router.get("/last_video")
async def get_last_video_report(background_tasks: BackgroundTasks, user=Depends(current_user),
								session=Depends(get_async_session)):

	stmt = select(video_tbl).order_by(video_tbl.c.title.desc()).limit(5)
	email_content = await session.execute(stmt)
	last_5_video = [i[1] for i in email_content.fetchall()]
	# for i in email_content.fetchall():
	# 	last_video.append(i[1])
	background_tasks.add_task(send_email_report_last_video, user.email, last_5_video)
	return {
		"status": 200,
		"data": "Письмо отправлено",
		"details": 'Названия последних 5 загруженных видеозаписей'
	}

