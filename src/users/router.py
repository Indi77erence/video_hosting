from typing import List

from fastapi import APIRouter, Depends

from .schemas import UpdateUser, GetDataUsers, DeleteUser
from .service import get_all_users, get_my_user, update_my_user, delete_my_user


router = APIRouter(
	prefix='/api',
	tags=['Users']
)


@router.get('/get_all_users', response_model=List[GetDataUsers])
async def get_all_users(answer=Depends(get_all_users)):
	return answer


@router.get('/get_my_user', response_model=List[GetDataUsers])
async def get_my_users(answer=Depends(get_my_user)):
	return answer


@router.put('/update_my_user', response_model=UpdateUser)
async def update_my_user(answer=Depends(update_my_user)):
	return answer


@router.delete('/delete_my_users')
async def delete_my_users(answer=Depends(delete_my_user)):
	return answer



