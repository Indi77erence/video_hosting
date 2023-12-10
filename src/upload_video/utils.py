import os
from pathlib import Path
from typing import IO, Generator
from uuid import uuid4

import aiofiles
from fastapi import Depends, UploadFile, HTTPException
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession


from src.auth.models import User
from src.database import get_async_session
from src.upload_video.schemas import UploadVideo


current_dir = os.path.dirname(os.path.abspath(__file__))


# Общая сессия
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
	yield SQLAlchemyUserDatabase(session, User)


# Запись файла в базу данных
async def save_video(user_id, video: UploadFile, title: str, description: str):
	if not os.path.exists(f"{current_dir}\\media\\user_id_{user_id}"):
		os.makedirs(f"{current_dir}\\media\\user_id_{user_id}")
	path_video = f"{current_dir}\\media\\user_id_{user_id}\\{uuid4()}.mp4"
	if video.content_type == 'video/mp4':
		await write_video(path_video, video)
	else:
		raise HTTPException(status_code=418, detail='Неверный формат файла!')
	info = UploadVideo(title=title, description=description)
	return path_video, info



async def write_video(path_video: str, video: UploadFile):
	async with aiofiles.open(path_video, 'wb') as buffer:
		data = await video.read()
		return await buffer.write(data)


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
