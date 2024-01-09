from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.comment.service import get_comments
from src.videos.service import get_my_video, get_all_info, get_all_video

router = APIRouter(
	prefix='/pages',
	tags=['Pages']
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory='src/templates')


@router.get('/home')
async def get_start_page(request: Request, videos=Depends(get_all_video)):
	# if not videos:
	# 	return templates.TemplateResponse("error_page.html", {"request": request,
	# 														  "videos": 'На хостинге пока нет видеозаписей'})
	return templates.TemplateResponse("home.html", {"request": request, "videos": videos})


@router.get('/my_video')
async def get_my_video_page(request: Request, videos=Depends(get_my_video)):
	# if videos is AttributeError:
	# 	return templates.TemplateResponse("error_page.html", {"request": request,
	# 														  "videos": 'Вы не авторизованы'})
	return templates.TemplateResponse("my_video.html", {"request": request, "videos": videos})


@router.get('/search_video')
async def get_search_page(request: Request):
	return templates.TemplateResponse("search_video.html", {"request": request})


@router.get('/log_in')
async def get_login_page(request: Request):
	return templates.TemplateResponse("login.html", {"request": request})


@router.get('/search_video/{video_title}')
async def get_search_video(request: Request, videos=Depends(get_all_info)):
	return templates.TemplateResponse("search_video.html", {"request": request, "videos": videos})


@router.get('/error_page/')
async def get_error_page(request: Request):
	return templates.TemplateResponse("error_page.html", {"request": request})


@router.get('/play_video/{id_video}')
async def play_video(request: Request, comments=Depends(get_comments), videos=Depends(get_all_info)):
	return templates.TemplateResponse("play.html", {"request": request,
													"videos": videos,
													"comments": comments})


@router.get('/register/')
async def get_register_page(request: Request):
	return templates.TemplateResponse("register.html", {"request": request})
