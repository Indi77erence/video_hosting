from typing import List
from fastapi import APIRouter, Depends
from .service import get_all_users, get_my_user, update_my_user, delete_my_user
from ..auth.base_config import current_user
from ..auth.manager import get_user_manager
from ..auth.models import User
from ..auth.schemas import MyUserCreate, UserRead

router = APIRouter(
	prefix='/api',
	tags=['Users']
)

@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_user)):
	return {"message": f"Hello {user.email}!"}


@router.get('/get_all_users', response_model=List[UserRead])
async def get_all_users(answer=Depends(get_all_users)):
	return answer


@router.get('/get_my_user', response_model=List[UserRead])
async def get_my_users(answer=Depends(get_my_user)):
	return answer


@router.patch('/update_my_user')
async def update_my_user(answer=Depends(update_my_user)):
	return answer


@router.delete('/delete_my_users')
async def delete_my_users(answer=Depends(delete_my_user)):
	return answer


# @router.post('/create_user')
# async def create_user(user_create: MyUserCreate, user_manager=Depends(get_user_manager)):
# 	user = await user_manager.create(user_create)
# 	return f"User created: {user.username}"



