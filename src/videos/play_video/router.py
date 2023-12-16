from fastapi import APIRouter, Depends,Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse
from src.database import get_async_session
from ..models import video as video_tbl
from .utils import open_file



router = APIRouter(
	prefix='/play_video',
	tags=['Play_video']
)


@router.get('/{video_title}')
async def play_video(request: Request, video_title: str,
					session: AsyncSession = Depends(get_async_session)) -> StreamingResponse:
	stmt = select(video_tbl).where(video_tbl.c.title == video_title)
	result = await session.execute(stmt)
	file = result.fetchall()[0][3]
	file, status_code, content_len, headers = await open_file(request, file)
	response = StreamingResponse(file, media_type='videos/mp4', status_code=status_code)
	response.headers.update({
		'Accept-Ranges': 'bytes',
		'Content-Length': str(content_len),
		**headers
	})
	return response

