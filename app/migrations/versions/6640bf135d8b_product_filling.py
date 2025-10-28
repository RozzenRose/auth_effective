"""product filling

Revision ID: 6640bf135d8b
Revises: 8b31d25fdb2c
Create Date: 2025-10-28 13:37:59.092031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6640bf135d8b'
down_revision: Union[str, Sequence[str], None] = '8b31d25fdb2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Получаем connection для выполнения сырых SQL запросов
    conn = op.get_bind()

    # Создаем 15 продуктов
    products_data = [
        {
            'owner_id': 3,
            'name': 'Смартфон iPhone 15',
            'description': 'Новый флагманский смартфон с улучшенной камерой',
            'price': 99900
        },
        {
            'owner_id': 3,
            'name': 'Ноутбук MacBook Pro',
            'description': 'Мощный ноутбук для работы и творчества',
            'price': 149900
        },
        {
            'owner_id': 3,
            'name': 'Наушники AirPods Pro',
            'description': 'Беспроводные наушники с шумоподавлением',
            'price': 24900
        },
        {
            'owner_id': 3,
            'name': 'Умные часы Apple Watch',
            'description': 'Смарт-часы с функцией отслеживания здоровья',
            'price': 32900
        },
        {
            'owner_id': 3,
            'name': 'Планшет iPad Air',
            'description': 'Универсальный планшет для работы и развлечений',
            'price': 59900
        },
        {
            'owner_id': 3,
            'name': 'Игровая консоль PlayStation 5',
            'description': 'Новейшая игровая консоль от Sony',
            'price': 49900
        },
        {
            'owner_id': 3,
            'name': 'Фотокамера Canon EOS R6',
            'description': 'Профессиональная зеркальная камера',
            'price': 189900
        },
        {
            'owner_id': 3,
            'name': 'Монитор Dell 27"',
            'description': '4K монитор для комфортной работы',
            'price': 45900
        },
        {
            'owner_id': 3,
            'name': 'Клавиатура Mechanical',
            'description': 'Игровая механическая клавиатура',
            'price': 8900
        },
        {
            'owner_id': 3,
            'name': 'Компьютерная мышь Logitech',
            'description': 'Беспроводная мышь с длительным временем работы',
            'price': 4500
        },
        {
            'owner_id': 3,
            'name': 'Внешний жесткий диск 2TB',
            'description': 'Портативный SSD накопитель',
            'price': 12900
        },
        {
            'owner_id': 3,
            'name': 'Роутер Wi-Fi 6',
            'description': 'Мощный маршрутизатор с поддержкой Wi-Fi 6',
            'price': 15900
        },
        {
            'owner_id': 3,
            'name': 'Электронная книга Kindle',
            'description': 'Читалка с E-ink дисплеем',
            'price': 11900
        },
        {
            'owner_id': 3,
            'name': 'Колонка JBL Portable',
            'description': 'Портативная Bluetooth колонка',
            'price': 8900
        },
        {
            'owner_id': 3,
            'name': 'Пауэрбанк 20000 mAh',
            'description': 'Мощное портативное зарядное устройство',
            'price': 3500
        }
    ]

    # Вставляем продукты в таблицу
    op.bulk_insert(
        sa.table('products',
                 sa.column('owner_id', sa.Integer),
                 sa.column('name', sa.String),
                 sa.column('description', sa.String),
                 sa.column('price', sa.Integer)
                 ),
        products_data
    )


def downgrade():
    # Удаляем все созданные продукты
    op.execute("DELETE FROM products")