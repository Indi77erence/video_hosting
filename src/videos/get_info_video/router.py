from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from ..models import video as video_tbl
from ...auth.models import User
from ...pages.schemas import GetSearchVideo, GetSearchVideoUser
from ...auth.base_config import current_user
from ...auth.models import User
import re

router = APIRouter(
	prefix='/api',
	tags=['Get_info_video']
)

SEARCH_PATTERN = r'\b\w+\b'


@router.get('/get_all_video')
async def get_all_video(session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user=data.user)
				   for data in rez_query]
	if not rezult_data:
		return {
			"status": 200,
			"message": 'Precondition Failed',
			"details": f"На хостинге нет загруженных видео, станьте первым!"
		}
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Все видео'
	}


@router.get('/get_video_by_id/{id_video}')
async def get_video_by_id(id_video: int,
						  session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl).where(video_tbl.c.id == id_video)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user=data.user) for data
				   in rez_query]
	if not rezult_data:
		return {
			"status": 200,
			"message": 'Precondition Failed',
			"details": f"Видео с id:{id_video} не существует!"
		}
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Видео с id: {id_video}'
	}


@router.get('/get_video_by_title/{video_title}')
async def get_video_by_title(video_title: str, session: AsyncSession = Depends(get_async_session)):
	title_for_search = re.findall(SEARCH_PATTERN, video_title)
	query = select(video_tbl)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user=data.user)
				   for data in rez_query for word in title_for_search
				   if word in data.title]
	if not rezult_data:
		return {
			"status": 200,
			"message": 'Precondition Failed',
			"details": f"Видео с названием ({video_title}) не существует!"
		}
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Все видео под названием {video_title}'
	}


@router.get('/get_video_by_description/{description}')
async def get_video_by_description(description: str,
								   session: AsyncSession = Depends(get_async_session)):
	desc_for_search = re.findall(SEARCH_PATTERN, description)
	query = select(video_tbl)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user=data.user)
				   for data in rez_query for word in desc_for_search
				   if word in data.description]
	# if set(search_words) & set(re.findall(SEARCH_PATTERN, data.description))

	if not rezult_data:
		return {
			"status": 200,
			"message": 'Precondition Failed',
			"details": f"Видео, в описании которых есть: ({description}) не существует!"
		}
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Видео в описании которых есть: {description}'
	}


@router.get('/get_my_video')
async def get_my_video(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
	query = select(video_tbl).where(video_tbl.c.user == user.id)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user=data.user) for data
				   in rez_query]
	if not rezult_data:
		return {
			"status": 200,
			"message": 'Precondition Failed',
			"details": f"Вы пока не загрузили ни одного видео"
		}
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Вcе ваши видео'
	}


@router.get('/get_user_video/{user_id}')
async def get_user_video(user_id: int, session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl).where(video_tbl.c.user == user_id)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideoUser(id=data.id, title=data.title, description=data.description, user_id=data.user)
				   for data in rez_query]
	if not rezult_data:
		return {
			"status": 200,
			"message": 'Precondition Failed',
			"details": f"У данного пользователя нет видео"
		}
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Все видео пользователя {user_id}'
	}
