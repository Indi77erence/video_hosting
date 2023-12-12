from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.videos.get_info_video.router import get_video

router = APIRouter(
	prefix='/pages',
	tags=['pages']
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory='src/templates')


@router.get('/home')
def get_start_page(request: Request):
	return templates.TemplateResponse("home.html", {"request": request})


@router.get('/my_video')
def get_my_video_page(request: Request):
	return templates.TemplateResponse("my_video.html", {"request": request})


@router.get('/search_video')
def get_search_page(request: Request,):
	return templates.TemplateResponse("search_video.html", {"request": request})


@router.get('/log_in')
def get_login_page(request: Request,):
	return templates.TemplateResponse("log_in.html", {"request": request})


@router.get('/search_video/{video_title}')
def get_found_video(request: Request, videos=Depends(get_video)):
	return templates.TemplateResponse("search_video.html", {"request": request, "videos": videos["data"]})
