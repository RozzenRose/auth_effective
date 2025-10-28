from app.database.models import User, RefreshTokenList
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert


async def add_refresh_token_in_db(db, user_id: int, token: str) -> None:
    data = insert(RefreshTokenList).values(
        owner_id=user_id,
        refresh_token=token).on_conflict_do_nothing()
    await db.execute(data)
    await db.commit()


async def delete_refresh_token_in_db(db, id) -> None:
    query = delete(RefreshTokenList).where(RefreshTokenList.owner_id == id)
    await db.execute(query)
    await db.commit()
