from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession


from .models import comment as comment_tbl
from src.database import get_async_session
from .schemas import UpdateComment, GetComment, AddComment
from ..auth.base_config import current_user


async def get_comment(id_video: int, session: AsyncSession = Depends(get_async_session)):
	query = select(comment_tbl).where(comment_tbl.c.video_id == id_video)
	rez_query = await session.execute(query)
	rezult_data = [GetComment(id=data.id, content=data.content, user_id=data.user_id, video_id=data.video_id)
				   for data in rez_query]
	if not rezult_data:
		raise HTTPException(status_code=200, detail="Видео с таким названием отсутствует")
	yield rezult_data


async def get_user_comment(user_id: int, session: AsyncSession = Depends(get_async_session)):
	query = select(comment_tbl).where(comment_tbl.c.user_id == user_id)
	rez_query = await session.execute(query)
	rezult_data = [GetComment(id=data.id, content=data.content, user_id=data.user_id, video_id=data.video_id)
				   for data in rez_query]
	if not rezult_data:
		raise HTTPException(status_code=200, detail="Пользователь ничего не комментировал")
	yield rezult_data


async def add_comment(id_video: int,
					  content: str,
					  user=Depends(current_user),
					  session: AsyncSession = Depends(get_async_session)
					  ):
	stmt = insert(comment_tbl).values(content=content, user_id=user.id, video_id=id_video)
	info = AddComment(id_video=id_video, content=content)
	await session.execute(stmt)
	await session.commit()
	return info


async def update_my_comment(id_comment: int,
							content: UpdateComment,
							user=Depends(current_user),
							session: AsyncSession = Depends(get_async_session)):
	rez_query = await session.execute(
		select(comment_tbl).where(comment_tbl.c.id == id_comment, comment_tbl.c.user_id == user.id))
	if not rez_query.scalars().all():
		yield HTTPException(status_code=403, detail="Доступ запрещен")
	stmt = update(comment_tbl).where(comment_tbl.c.id == id_comment).values(content.dict())
	await session.execute(stmt)
	await session.commit()
	yield content


async def delete_my_comment(id_comment: int,
					   user=Depends(current_user),
					   session: AsyncSession = Depends(get_async_session)):
	rez_query = await session.execute(
		select(comment_tbl).where(comment_tbl.c.id == id_comment, comment_tbl.c.user_id == user.id))
	if not rez_query.scalars().all():
		raise HTTPException(status_code=403, detail="Вы не имеете прав доступа к данному комментарию!")
	stmt = delete(comment_tbl).where(comment_tbl.c.id == id_comment)
	await session.execute(stmt)
	await session.commit()
	return {
		"status": 200,
		"details": f'Комментарий с id:{id_comment} удален'
	}