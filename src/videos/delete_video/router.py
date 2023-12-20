from fastapi import HTTPException
from fastapi import APIRouter, Depends, Query
from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from ..models import video as video_tbl
from ...auth.base_config import current_user

router = APIRouter(
	prefix='/api',
	tags=['Delete_video']
)


@router.delete('/delete_video/{id_video}')
async def delete_video(id_video: int,
					    user=Depends(current_user),
						session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl).where(video_tbl.c.id == id_video, video_tbl.c.user == user.id)
	rez_query = await session.execute(query)
	if not rez_query.scalars().all():
		raise HTTPException(status_code=403, detail="Вы не имеете прав доступа к данному видео!")
	stmt = delete(video_tbl).where(video_tbl.c.id == id_video)
	await session.execute(stmt)
	await session.commit()
	return {
		"status": 200,
		"details": f'Видео с id:{id_video} удалено'
	}



