from typing import List
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Depends
from src.comment.schemas import UpdateComment, GetComment, GetCommentsForVideo
from src.comment.service import update_my_comment, add_comment, get_user_comment, get_comments, delete_my_comment


router = APIRouter(
	prefix='/api',
	tags=['Comment']
)
templates = Jinja2Templates(directory='src/templates')


@router.get("/get_video_comment/{id_video}", response_model=List[GetCommentsForVideo])
async def get_comment(answer=Depends(get_comments)):
	return answer


@router.get("/get_user_comment/{user_id}", response_model=List[GetComment])
async def get_user_comment(answer=Depends(get_user_comment)):
	return answer


@router.get("/get_user_comment/{content}", response_model=List[GetComment])
async def get_user_comment(answer=Depends(get_user_comment)):
	return answer


@router.post("/add_comment")
async def add_comments(answer=Depends(add_comment)):
	return answer


@router.patch("/update_my_comment/{id_video}", response_model=UpdateComment)
async def update_my_comment(answer=Depends(update_my_comment)):
	return answer


@router.delete("/delete_my_comment/{id_comment}")
async def delete_my_comment(answer=Depends(delete_my_comment)):
	return answer
