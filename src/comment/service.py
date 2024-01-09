from fastapi import HTTPException, Form
from fastapi import Depends
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from .models import comment as comment_tbl
from src.database import get_async_session
from .schemas import UpdateComment, GetComment, AddComment, GetCommentsForVideo
from ..auth.base_config import current_user
from ..auth.models import user as user_tbl


async def get_comments(id_video: int, session: AsyncSession = Depends(get_async_session)):
	query = select(user_tbl.c.username, comment_tbl.c.content).join(comment_tbl).where(
		comment_tbl.c.video_id == id_video)
	rez_query = await session.execute(query)
	rezult_data = [GetCommentsForVideo(username=data.username, content=data.content)
				   for data in rez_query]
	# if not rezult_data:
	# 	raise HTTPException(status_code=200, detail="Комментариев к видео нет")
	return rezult_data


async def get_user_comment(user_id: int, session: AsyncSession = Depends(get_async_session)):
	query = select(comment_tbl).where(comment_tbl.c.user_id == user_id)
	rez_query = await session.execute(query)
	rezult_data = [GetComment(id=data.id, content=data.content, user_id=data.user_id, video_id=data.video_id)
				   for data in rez_query]
	if not rezult_data:
		raise HTTPException(status_code=200, detail="Пользователь ничего не комментировал")
	return rezult_data


async def add_comment(user=Depends(current_user),
					  id_video: int = Form(...),
					  content: str = Form(...),
					  session: AsyncSession = Depends(get_async_session)
					  ):
	stmt = insert(comment_tbl).values(content=content, video_id=id_video, user_id=user.id)
	await session.execute(stmt)
	await session.commit()
	info = AddComment(id_video=id_video, content=content)
	return info


async def update_my_comment(id_comment: int,
							content: UpdateComment,
							user=Depends(current_user),
							session: AsyncSession = Depends(get_async_session)):
	rez_query = await session.execute(
		select(comment_tbl).where(comment_tbl.c.id == id_comment, comment_tbl.c.user_id == user.id))
	if not rez_query.scalars().all():
		return HTTPException(status_code=403, detail="Доступ запрещен")
	stmt = update(comment_tbl).where(comment_tbl.c.id == id_comment).values(content.dict())
	await session.execute(stmt)
	await session.commit()
	return content


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
