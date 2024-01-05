from typing import List

from fastapi import APIRouter, Depends
from starlette.templating import Jinja2Templates

from .schemas import GetSearchVideo, UploadVideo, UpdateVideo
from .service import get_all_info, get_my_video, upload_video, update_video, delete_video, play_video

router = APIRouter(
	prefix='/api',
	tags=['Video']
)

templates = Jinja2Templates(directory='src/templates')


@router.get("/get_all_info_video", response_model=List[GetSearchVideo])
async def get_all_info(answer=Depends(get_all_info)):
	return answer


@router.get("/get_all_my_video", response_model=List[GetSearchVideo])
async def get_my_video(answer=Depends(get_my_video)):
	return answer


@router.post("/upload_video", response_model=UploadVideo)
async def upload_video(answer=Depends(upload_video)):
	return answer


@router.patch("/update_my_video/{id_video}", response_model=UpdateVideo)
async def update_my_video(answer=Depends(update_video)):
	return answer


@router.delete("/delete_my_video/{id_video}")
async def delete_my_video(answer=Depends(delete_video)):
	return answer


@router.get("/play_video/{video_title}")
async def play_video(answer=Depends(play_video)):
	return answer


