from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from app.database.db_depends import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.functions.auth_functions import get_current_user
from app.schemas import CreateProduct
from app.database.db_functions import create_product_in_db, get_all_products_in_db
from app.redis_inf import Redis


router = APIRouter(prefix='/products', tags=['products'])


@router.post("/create_product")
async def create_product(db: Annotated[AsyncSession, Depends(get_db)],
                         user: Annotated[dict, Depends(get_current_user)],
                         product: CreateProduct):
    '''Создаем товары, если мы продавец'''
    redis = await Redis.get_redis()
    did_u_logout = await redis.get(f'{user.get("user_id")}')
    if did_u_logout == user.get("token"): # проверяем, нет ли в блек листе текущего access
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is logged out')
    if not user.get("is_seller"): # проверяем, что юзер - продавец
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='User is not seller')
    await create_product_in_db(db, user.get("user_id"), product) # Добавляем товар в БД
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Product created successfully'}


@router.get("/get_all_products")
async def get_all_products(db: Annotated[AsyncSession, Depends(get_db)],
                           user: Annotated[dict, Depends(get_current_user)]):
    '''Получаем все товары, если мы покупатель'''
    redis = await Redis.get_redis()
    did_u_logout = await redis.get(f'{user.get("user_id")}')
    if did_u_logout == user.get("token"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is logged out')
    if not user.get("is_buyer"): # проверяем, что юзер - покупатель
        raise HTTPException(status_code=status.status.HTTP_403_FORBIDDEN,
                            detail='User is not buyer')
    products = await get_all_products_in_db(db) # Достаем все товары из БД
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Products get successfully',
            'products': products}
