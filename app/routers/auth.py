from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from app.database.db_depends import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import CreateUser
from app.database.db_functions import create_user_in_db, get_user
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.functions.hashing import pass_hasher, pass_verify
from app.functions.auth_functions import (create_access_token, get_current_user,
                                          create_refresh_token, verify_refresh_token)
from datetime import timedelta


router = APIRouter(prefix='/auth', tags=['auth'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


@router.get("/me")
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await get_current_user(token)
    return {"user_id": user.get('user_id'),
            "username": user.get('username'),
            "email": user.get('email'),}


@router.post('/create_user', status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[AsyncSession, Depends(get_db)], create_user: CreateUser):
    hashed_password = await pass_hasher(create_user.password)
    await create_user_in_db(db, create_user, hashed_password)
    return {'status_code':status.HTTP_201_CREATED,
            'transaction': 'User created successfully'}


@router.post('/token')
async def login(db: Annotated[AsyncSession, Depends(get_db)],
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_user(db, form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is not exist')
    if not await pass_verify(user.hashed_password, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid password')
    token = await create_access_token(user.id, user.username,
                                      user.email, user.is_admin,
                                      expires_delta=timedelta(minutes=20))
    refresh_token = await create_refresh_token(user.username)
    return {'access_token': token,
            'refresh_token': refresh_token,
            'token_type': 'bearer'}


@router.post('/refresh')
async def refresh_tokens(db: Annotated[AsyncSession, Depends(get_db)],
                        refresh_token: str):
    username = await verify_refresh_token(refresh_token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid refresh token')
    user = await get_user(db, username)
    access_token = await create_access_token(user.id, user.username,
                                             user.email, user.is_admin,
                                             expires_delta=timedelta(minutes=20))
    new_refresh_token = await create_refresh_token(user.username)
    return {'access_token': access_token,
            'refresh_token': new_refresh_token,
            'token_type': 'bearer'}