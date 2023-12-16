from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from ..auth.base_config import current_user
from ..auth.models import User
from ..auth.schemas import GetAllUsers
from ..pages.schemas import GetSearchVideo, GetSearchVideoUser
from ..videos.models import video as video_tbl

router = APIRouter(
	prefix='/api',
	tags=['Get info users']
)


@router.get('/get_all_users')
async def get_all_user(session: AsyncSession = Depends(get_async_session)):
	query = select(User).where()
	rez_query = await session.execute(query)
	rezult_data = [GetAllUsers(id=user[0].id, email=user[0].email, username=user[0].username)
				   for user in rez_query]
	if not rezult_data:
		return {
			"status": 200,
			"message": 'Precondition Failed',
			"details": f"На хостинге нет пользователей"
		}
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Все видео'
	}


@router.get('/get_my_user')
async def get_my_user(session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
	query = select(User).where(User.id == user.id)
	rez_query = await session.execute(query)
	rezult_data = [GetAllUsers(id=user[0].id, email=user[0].email, username=user[0].username)
				   for user in rez_query]
	if not rezult_data:
		raise HTTPException(status_code=403, detail="Доступ запрещен")
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Все видео'
	}
