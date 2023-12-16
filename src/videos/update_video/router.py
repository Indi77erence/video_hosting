from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from ..models import video as video_tbl
from ..schemas import UpdateVideo

router = APIRouter(
	prefix='/api',
	tags=['Update_video']
)


@router.put('/update_video')
async def update_video(id_video: int,
						values: UpdateVideo,
						session: AsyncSession = Depends(get_async_session)):
	stmt = update(video_tbl).where(video_tbl.c.id == id_video).values(**values.model_dump(exclude_none=True))
	await session.execute(stmt)
	await session.commit()
	return {
		"status": 200,
		"details": f'Изменение прошло успешно'
	}


