import os
import re
from typing import Optional
from uuid import uuid4
from pathlib import Path
from typing import IO, Generator
import aiofiles
from fastapi import HTTPException, UploadFile, Form, File
from fastapi import Depends, Request
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse
from .models import video as video_tbl
from src.database import get_async_session
from .schemas import GetSearchVideo, UploadVideo, UpdateVideo, PlayVideo
from ..auth.base_config import current_user

SEARCH_PATTERN = r'\b\w+\b'
current_dir = os.path.dirname(os.path.abspath(__file__))


async def get_all_info(id_video: Optional[int] = None,
					   video_title: Optional[str] = None,
					   description: Optional[str] = None,
					   user_id: Optional[int] = None,
					   session: AsyncSession = Depends(get_async_session)):
	if id_video and not video_title and not description:
		query = select(video_tbl).where(video_tbl.c.id == id_video)
		rez_query = await session.execute(query)
		rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user_id=data.user_id,
									  preview=data.preview) for data in rez_query]
		return rezult_data


	elif video_title and not id_video and not description:
		title_for_search = re.findall(SEARCH_PATTERN, video_title)
		query = select(video_tbl)
		rez_query = await session.execute(query)
		rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user_id=data.user_id,
									  preview=data.preview) for data in rez_query for word in title_for_search
					   if word in data.title]

		return rezult_data

	elif description and not video_title and not id_video:
		desc_for_search = re.findall(SEARCH_PATTERN, description)
		query = select(video_tbl)
		rez_query_desc = await session.execute(query)
		rezult_data_desc = [
			GetSearchVideo(id=data.id, title=data.title, description=data.description, user_id=data.user_id,
						   preview=data.preview)
			for data in rez_query_desc for word in desc_for_search
			if word in data.description]
		# if set(search_words) & set(re.findall(SEARCH_PATTERN, data.description))
		return rezult_data_desc

	elif video_title and description:
		title_for_search = re.findall(SEARCH_PATTERN, video_title)
		desc_for_search = re.findall(SEARCH_PATTERN, description)
		query = select(video_tbl)
		rez_query = await session.execute(query)
		rezult_data_title = [
			GetSearchVideo(id=data.id, title=data.title, description=data.description, user_id=data.user_id,
						   preview=data.preview)
			for data in rez_query for word in title_for_search
			if word in data.title]
		rezult_all_data = [
			GetSearchVideo(id=data.id, title=data.title, description=data.description, user_id=data.user_id,
						   preview=data.preview)
			for data in rezult_data_title for word in desc_for_search
			if word in data.description]
		return rezult_all_data

	elif user_id:
		query = select(video_tbl).where(video_tbl.c.user_id == user_id)
		rez_query = await session.execute(query)
		rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user_id=data.user_id,
									  preview=data.preview)
					   for data in rez_query]
		return rezult_data

	else:
		rezult_data = [{"info": "На хостинге нет загруженных видео"}]
		return rezult_data


async def get_my_video(session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
	query = select(video_tbl).where(video_tbl.c.user_id == user.id)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user_id=data.user_id,
								  preview=data.preview) for data in rez_query]
	return rezult_data


async def get_all_video(session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchVideo(id=data.id, title=data.title, description=data.description, user_id=data.user_id,
								  preview=data.preview) for data in rez_query]
	# if not rezult_data:
	# 	raise HTTPException(status_code=200, detail="На хостинге нет загруженных видео")
	return rezult_data


async def update_video(id_video: int,
					   values: UpdateVideo = None,
					   user=Depends(current_user),
					   session: AsyncSession = Depends(get_async_session)):
	rez_query = await session.execute(
		select(video_tbl).where(video_tbl.c.id == id_video, video_tbl.c.user_id == user.id))
	if not rez_query.scalars().all():
		return HTTPException(status_code=403, detail="Доступ запрещен")
	stmt = update(video_tbl).where(video_tbl.c.id == id_video).values(values.dict())
	await session.execute(stmt)
	await session.commit()
	return values


async def delete_video(id_video: int,
					   user=Depends(current_user),
					   session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl).where(video_tbl.c.id == id_video, video_tbl.c.user_id == user.id)
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


async def upload_video(user=Depends(current_user),
					   title: str = Form(...),
					   preview: UploadFile = File(...),
					   video: UploadFile = File(...),
					   description: str = None,
					   session: AsyncSession = Depends(get_async_session)
					   ):
	path_video, path_preview, info = await save_video(user.id, preview, video, title, description)
	stmt = insert(video_tbl).values(file=path_video, preview=path_preview, user_id=user.id, **info.dict())
	await session.execute(stmt)
	await session.commit()
	return info


async def save_video(user_id, preview: UploadFile, video: UploadFile, title: str, description: str):
	if not os.path.exists(f"{os.path.abspath(os.curdir)}\\src\\videos\\users_video\\user_id_{user_id}"):
		os.makedirs(f"{os.path.abspath(os.curdir)}\\src\\videos\\users_video\\user_id_{user_id}")
	path_video = f"{os.path.abspath(os.curdir)}\\src\\videos\\users_video\\user_id_{user_id}\\{uuid4()}.mp4"
	path_preview = f"{os.path.abspath(os.curdir)}\\src\\videos\\users_video\\static\\{uuid4()}.png"
	await write_video(path_video, video)
	await write_preview(path_preview, preview)
	info = UploadVideo(title=title, description=description, user_id=user_id)
	return path_video, os.path.basename(path_preview), info


async def write_video(path_video: str, video: UploadFile):
	async with aiofiles.open(path_video, 'wb') as buffer:
		data_video = await video.read()
		return await buffer.write(data_video)


async def write_preview(path_preview: str, preview: UploadFile):
	async with aiofiles.open(path_preview, 'wb') as buffer:
		data_preview = await preview.read()
		return await buffer.write(data_preview)


async def play_video(id_video: int, request: Request,
					 session: AsyncSession = Depends(get_async_session)) -> StreamingResponse:
	stmt = select(video_tbl).where(video_tbl.c.id == id_video)
	result = await session.execute(stmt)
	file = result.fetchone()[4]
	file, status_code, content_len, headers = await open_file(request, file)
	response = StreamingResponse(file, media_type='videos/mp4', status_code=status_code)
	response.headers.update({
		'Accept-Ranges': 'bytes',
		'Content-Length': str(content_len),
		**headers
	})
	return response


async def open_file(request, file):
	def ranged(
			file: IO[bytes],
			start: int = 0,
			end: int = None,
			block_size: int = 8192,
	) -> Generator[bytes, None, None]:
		consumed = 0

		file.seek(start)

		while True:
			data_length = min(block_size, end - start - consumed) if end else block_size

			if data_length <= 0:
				break

			data = file.read(data_length)

			if not data:
				break

			consumed += data_length

			yield data

		if hasattr(file, 'close'):
			file.close()

	path = Path(file)
	file = path.open('rb')
	file_size = path.stat().st_size

	content_len = file_size
	satus_code = 200
	headers = {}
	content_range = request.headers.get('range')

	if content_range is not None:
		content_range = content_range.strip().lower()
		content_ranges = content_range.split('=')[-1]
		range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
		range_start = max(0, int(range_start)) if range_start else 0
		range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
		content_len = (range_end - range_start) + 1
		file = ranged(file, start=range_start, end=range_end + 1)
		satus_code = 206
		headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

	return file, satus_code, content_len, headers


async def get_video_title(video_title: str, session: AsyncSession = Depends(get_async_session)):
	query = select(video_tbl).where(video_tbl.c.title == video_title)
	rez_query = await session.execute(query)
	rezult_data = [PlayVideo(title=data.title, preview=data.preview) for data in rez_query]
	if not rezult_data:
		raise HTTPException(status_code=200, detail="Видео с таким названием отсутствует")
	return rezult_data
