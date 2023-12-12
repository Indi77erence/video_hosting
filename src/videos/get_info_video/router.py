from fastapi import APIRouter, Depends, Form, UploadFile, File, Request

from sqlalchemy import select, insert, Row

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from ..models import video as video_tbl

from ...pages.schemas import GetSearchVideo

router = APIRouter(
	prefix='/get_info_video',
	tags=['Get_info_video']
)


@router.get('/get_video')
async def get_video(video_title: str,
					session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl).where(video_tbl.c.title == video_title)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(title=data.title, description=data.description) for data in rez_query]
	return {
		"status": 200,
		"data": rezult_data,
		"details": f'Все видео под названием {video_title}'
	}

# @router.get('/user/all_video/', response_model=List[CreateVideo])
# async def get_list_video_user(session: AsyncSession = Depends(get_async_session)):
# 	query = select(videos).where()
# 	video_list = await videos.e
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
