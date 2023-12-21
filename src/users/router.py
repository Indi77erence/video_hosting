from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from ..auth.base_config import current_user
from ..auth.models import User
from ..auth.schemas import GetAllUsers

router = APIRouter(
	prefix='/api',
	tags=['Users']
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
		"details": f'Это данные вашего пользователя'
	}


# @router.put('/update_my_user')
# async def get_my_user(email: str = None, username: str = None, session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
# 	print(user.id)
# 	rez_query = await session.execute(select(User).where(User.id == user.id))
# 	if not rez_query.scalars().all():
# 		return HTTPException(status_code=403, detail="Доступ запрещен")
# 	query = f"UPDATE user SET email={email}, username={username} WHERE id={user.id}"
# 	await session.execute(query)
# 	await session.commit()
# 	return {
# 		"status": 200,
# 		"details": f'Изменение прошло успешно!'
# 	}

