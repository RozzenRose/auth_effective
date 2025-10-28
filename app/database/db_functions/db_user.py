from app.database.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update


async def create_user_in_db(db, user_data: CreateUser, hashed_password: str) -> None:
    data = insert(User).values(
        firstname=user_data.firstname,
        fathername=user_data.fathername,
        lastname=user_data.lastname,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password)
    await db.execute(data)
    await db.commit()


async def get_user(db, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def update_user_options_in_db(db, user_data: UpdateUser):
    query = update(User).where(User.id == user_data.target_user_id).values(
        is_seller=user_data.is_seller,
        is_buyer=user_data.is_buyer)
    await db.execute(query)
    await db.commit()


async def disactivate_user_in_db(db, user_id):
    query = update(User).where(User.id == user_id).values(is_activate=False)
    await db.execute(query)
    await db.commit()
