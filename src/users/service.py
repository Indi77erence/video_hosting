from fastapi import Depends, HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.auth.schemas import UserRead
from src.database import get_async_session
from src.users.schemas import GetDataUsers, UpdateUser


async def get_all_users(session: AsyncSession = Depends(get_async_session)):
	query = select(User)
	rez_query = await session.execute(query)
	rezult_data = [UserRead(id=user[0].id, email=user[0].email, username=user[0].username,
							role_id=user[0].role_id, is_active=user[0].is_active,
							is_superuser=user[0].is_superuser, is_verified=user[0].is_verified)
				   			for user in rez_query]
	if not rezult_data:
		raise HTTPException(status_code=403, detail="На ресурсе нет зарегистрированных пользователей!")
	yield rezult_data


async def get_my_user(session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
	query = select(User).where(User.id == user.id)
	rez_query = await session.execute(query)
	rezult_data = [UserRead(id=user[0].id, email=user[0].email, username=user[0].username,
							role_id=user[0].role_id,is_active=user[0].is_active,
							is_superuser=user[0].is_superuser,is_verified=user[0].is_verified)
				   			for user in rez_query]
	if not rezult_data:
		raise HTTPException(status_code=403, detail="Доступ запрещен")
	yield rezult_data


async def update_my_user(values: UpdateUser = None, session: AsyncSession = Depends(get_async_session),
						 user=Depends(current_user)):
	query = select(User).where(User.id == user.id)
	rez_query = await session.execute(query)
	if not rez_query.first()[0].username:
		yield HTTPException(status_code=403, detail="Доступ запрещен")
	stmt = update(User).where(User.id == user.id).values(values.dict(exclude_none=True))
	await session.execute(stmt)
	await session.commit()
	yield values


async def delete_my_user(session: AsyncSession = Depends(get_async_session),
						 user=Depends(current_user)):
	query = select(User).where(User.id == user.id)
	rez_query = await session.execute(query)
	if not rez_query.first()[0].username:
		yield HTTPException(status_code=403, detail="Доступ запрещен")
	stmt = delete(User).where(User.id == user.id)
	await session.execute(stmt)
	await session.commit()
	yield "Пользователь удален!"
