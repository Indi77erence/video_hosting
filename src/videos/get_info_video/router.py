from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from ..models import video as video_tbl
from ...auth.models import User
from ...pages.schemas import GetSearchVideo
from ...auth.base_config import current_user

router = APIRouter(
	prefix='/api',
	tags=['Get_info_video']
)


@router.get('/get_video_by_description')
async def get_video_by_description(description: str,
								   session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description) for data in rez_query
				   if description.lower() in data.description.lower()]
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Видео в описании которых есть: {description}'
	}


@router.get('/get_video_by_id')
async def get_video_by_id(id_video: int,
						  session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl).where(video_tbl.c.id == id_video)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description) for data in rez_query]

	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Видео с id: {id_video}'
	}


@router.get('/get_video_by_title')
async def get_video_by_title(video_title: str,
							 session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl).where(video_tbl.c.title == video_title)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description) for data in rez_query]
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Все видео под названием {video_title}'
	}


@router.get('/get_all_video')
async def get_all_video(session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl).where()
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description) for data in rez_query]
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Все видео'
	}


@router.get('/get_my_video')
async def get_my_video(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
	query = select(video_tbl).where(video_tbl.c.user == user.id)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description) for data in rez_query]
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Вcе ваши видео'
	}
