from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from ..database import get_async_session
from ..videos.models import video as video_tbl
from .service import send_email_report_last_video
from ..auth.base_config import current_user

router = APIRouter(
	prefix='/api',
	tags=['Back_tasks']
)


@router.get("/last_five_video")
async def send_email_last_upload_video(background_tasks: BackgroundTasks, user=Depends(current_user),
								session=Depends(get_async_session)):
	query = select(video_tbl).order_by(video_tbl.c.title.desc()).limit(5)
	email_content = await session.execute(query)
	last_five_video = [i[1] for i in email_content.fetchall()]
	background_tasks.add_task(send_email_report_last_video, user.email, last_five_video)

	return {
		"status": 200,
		"data": "Письмо отправлено",
		"details": 'Названия последних 5 загруженных видеозаписей'
	}
