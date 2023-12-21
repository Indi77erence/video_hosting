from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from ..models import video as video_tbl
from ...auth.models import User
from ...pages.schemas import GetSearchVideo, GetSearchVideoUser
from ...auth.base_config import current_user
import re

router = APIRouter(
	prefix='/api',
	tags=['Videos']
)

SEARCH_PATTERN = r'\b\w+\b'


@router.get("/all_info")
async def get_all_info(id_video: Optional[int] = None,
					   video_title: Optional[str] = None,
					   description: Optional[str] = None,
					   user_id: Optional[int] = None,
					   session: AsyncSession = Depends(get_async_session)):
	if id_video and not video_title and not description:
		query = select(video_tbl).where(video_tbl.c.id == id_video)
		rez_query = await session.execute(query)
		rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user=data.user)
					   for data in rez_query]
		return {
			"status": 200,
			"data": rezult_data,
			"details": f'Видео с id: {id_video}'
		}

	elif video_title and not id_video and not description:
		title_for_search = re.findall(SEARCH_PATTERN, video_title)
		query = select(video_tbl)
		rez_query = await session.execute(query)
		rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user=data.user)
					   for data in rez_query for word in title_for_search
					   if word in data.title]
		print(rezult_data)
		return {
			"status": 200,
			"data": rezult_data,
			"details": f'Все видео в названии которых есть: {video_title}'
		}

	elif description and not video_title and not id_video:
		desc_for_search = re.findall(SEARCH_PATTERN, description)
		query = select(video_tbl)
		rez_query_desc = await session.execute(query)
		rezult_data_desc = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user=data.user)
							for data in rez_query_desc for word in desc_for_search
							if word in data.description]
		# if set(search_words) & set(re.findall(SEARCH_PATTERN, data.description))
		return {
			"status": 200,
			"data": rezult_data_desc,
			"details": f'Все видео в описании которых есть: {description}'
		}

	elif user_id:
		query = select(video_tbl).where(video_tbl.c.user == user_id)
		rez_query = await session.execute(query)
		rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user=data.user)
					   for data in rez_query]
		return {
			"status": 200,
			"data": rezult_data,
			"details": f"Все видео пользователя с id: {user_id}"
		}

	else:
		return {
			"status": 200,
			"message": 'Precondition Failed',
			"details": f"На хостинге нет загруженных видео, станьте первым!"
		}


@router.get('/get_my_video')
async def get_my_video(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
	query = select(video_tbl).where(video_tbl.c.user == user.id)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user=data.user) for
				   data
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