import os
from uuid import uuid4

import aiofiles
from fastapi import Depends, UploadFile, HTTPException
from src.videos.schemas import UploadVideo


current_dir = os.path.dirname(os.path.abspath(__file__))


# Запись видео в базу данных
async def save_video(user_id, video: UploadFile, title: str, description: str):
	if not os.path.exists(f"{current_dir}\\users_video\\user_id_{user_id}"):
		os.makedirs(f"{current_dir}\\users_video\\user_id_{user_id}")
	path_video = f"{current_dir}\\users_video\\user_id_{user_id}\\{uuid4()}.mp4"
	await write_video(path_video, video)
	info = UploadVideo(title=title, description=description)
	return path_video, info



async def write_video(path_video: str, video: UploadFile):
	async with aiofiles.open(path_video, 'wb') as buffer:
		data = await video.read()
		return await buffer.write(data)

