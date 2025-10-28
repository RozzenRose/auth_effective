from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from app.database.db_depends import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.functions.auth_functions import get_current_user
from app.schemas import CreateProduct
from app.database.db_functions import create_product_in_db


router = APIRouter(prefix='/products', tags=['products'])


@router.post("/create_product")
async def create_product(db: Annotated[AsyncSession, Depends(get_db)],
                         user: Annotated[dict, Depends(get_current_user)],
                         product: CreateProduct):
    if not user.get("is_seller"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is not seller')
    await create_product_in_db(db, user.get("user_id"), product)
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Product created successfully'}
