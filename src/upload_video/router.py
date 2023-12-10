import time
from pathlib import Path

from fastapi import APIRouter, Depends, Form, UploadFile, File, Request
from fastapi_cache.decorator import cache

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates
from src.database import get_async_session
from .models import video as video_tbl
from .utils import save_video, open_file

router = APIRouter(
	prefix='/video',
	tags=['Video']
)
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@router.get('/any_long_operation')
@cache(expire=3600)
def get_long_op():
	time.sleep(3)
	return 'Много-много данных!'


@router.post('/upload_video')
async def upload_video(
		user_id: int,
		title: str = Form(...),
		description: str = Form(...),
		video: UploadFile = File(...),
		session: AsyncSession = Depends(get_async_session)
):
	path_video, info = await save_video(user_id, video, title, description)
	stmt = insert(video_tbl).values(file=path_video, user=user_id, **info.dict())
	await session.execute(stmt)
	await session.commit()
	return info


@router.get('/{video_pk}')
async def get_video(request: Request, video_pk: int,
					session: AsyncSession = Depends(get_async_session)) -> StreamingResponse:
	stmt = select(video_tbl).where(video_tbl.c.id == video_pk)
	result = await session.execute(stmt)
	file = result.fetchall()[0][3]
	file, status_code, content_len, headers = await open_file(request, file)
	response = StreamingResponse(file, media_type='video/mp4', status_code=status_code)
	response.headers.update({
		'Accept-Ranges': 'bytes',
		'Content-Length': str(content_len),
		**headers
	})
	return response

# @router.get('/user/all_video/', response_model=List[CreateVideo])
# async def get_list_video_user(session: AsyncSession = Depends(get_async_session)):
# 	query = select(video).where()
# 	video_list = await video.e
# 	return video_list


# @router.get('/')
# async def get_all_video_(operation_type: str, session: AsyncSession = Depends(get_async_session)):
# 	try:
# 		query = select(operation).where(operation.c.type == operation_type)
# 		rez_query = await session.execute(query)
# 		rezult_data = [GetOperation(id=data.id, quantity=data.quantity, figi=data.figi, instrument_type=data.instrument_type,
# 								date=data.date, type=data.type) for data in rez_query]
# 		return {
# 			"status": "success",
# 			"data": rezult_data,
# 			"details": None
# 		}
# 	except Exception:
# 		raise HTTPException(status_code=500, detail={
# 			"status": "error",
# 			"data": None,
# 			"details": None
# 		})
#
#
# @router.post('/asd')
# async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
# 	stmt = insert(operation).values(**new_operation.model_dump())
# 	await session.execute(stmt)
# 	await session.commit()
# 	return {'status': 'OK'}
