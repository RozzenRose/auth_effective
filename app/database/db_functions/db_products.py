from app.database.models import Product
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from app.schemas import CreateProduct


async def create_product_in_db(db, user_id: int, product_data: CreateProduct) -> None:
    data = insert(Product).values(
        owner_id=user_id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price)
    await db.execute(data)
    await db.commit()

