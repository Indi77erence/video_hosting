from fastapi import APIRouter, BackgroundTasks, Depends

from .tasks import send_email_report_last_video
from ..auth.base_config import current_user


router = APIRouter(prefix="/report")


@router.get("/last_video")
def get_last_video_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
	background_tasks.add_task(send_email_report_last_video, user.email)
	return {
		"status": 200,
		"data": "Письмо отправлено",
		"details": 'Названия последних 5 загруженных видеозаписей'
	}