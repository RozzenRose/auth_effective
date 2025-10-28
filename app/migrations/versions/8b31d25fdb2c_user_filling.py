"""user filling

Revision ID: 8b31d25fdb2c
Revises: 82817e71a1ee
Create Date: 2025-10-28 13:28:37.496145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base


# revision identifiers, used by Alembic.
revision: str = '8b31d25fdb2c'
down_revision: Union[str, Sequence[str], None] = '82817e71a1ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    firstname = sa.Column(sa.String, nullable=False)
    fathername = sa.Column(sa.String, nullable=False)
    lastname = sa.Column(sa.String, nullable=False)
    username = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    is_activate = sa.Column(sa.Boolean, default=True)
    is_admin = sa.Column(sa.Boolean, default=False)
    is_seller = sa.Column(sa.Boolean, default=False)
    is_buyer = sa.Column(sa.Boolean, default=True)


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # Хешированные пароли (в реальном приложении используйте bcrypt или аналоги)
    # Здесь простой пример - в продакшене обязательно хешируйте пароли правильно
    hashed_password_example = "hashed_password_123"

    # Пользователь 1: Администратор
    admin_user = User(
        firstname="Иван",
        fathername="Иванович",
        lastname="Иванов",
        username="admin_user",
        email="admin@example.com",
        hashed_password='$argon2id$v=19$m=262144,t=3,p=2$tYeqGQ8PAsIzKIGgdz0iSA$QfleDVFLOEekIZCEvdHPZ84FnpijxV/YnCKARJvYQ2w',
        is_activate=True,
        is_admin=True,
        is_seller=False,
        is_buyer=False
    )

    # Пользователь 2: Только покупатель
    buyer_user = User(
        firstname="Петр",
        fathername="Петрович",
        lastname="Петров",
        username="buyer_user",
        email="buyer@example.com",
        hashed_password='$argon2id$v=19$m=262144,t=3,p=2$tYeqGQ8PAsIzKIGgdz0iSA$QfleDVFLOEekIZCEvdHPZ84FnpijxV/YnCKARJvYQ2w',
        is_activate=True,
        is_admin=False,
        is_seller=False,
        is_buyer=True
    )

    # Пользователь 3: Только продавец
    seller_user = User(
        firstname="Сергей",
        fathername="Сергеевич",
        lastname="Сергеев",
        username="seller_user",
        email="seller@example.com",
        hashed_password='$argon2id$v=19$m=262144,t=3,p=2$tYeqGQ8PAsIzKIGgdz0iSA$QfleDVFLOEekIZCEvdHPZ84FnpijxV/YnCKARJvYQ2w',
        is_activate=True,
        is_admin=False,
        is_seller=True,
        is_buyer=False
    )

    # Добавляем пользователей в сессию
    session.add_all([admin_user, buyer_user, seller_user])
    session.commit()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # Удаляем созданных пользователей
    session.execute(
        sa.text("DELETE FROM users WHERE email IN (:email1, :email2, :email3)"),
        {
            'email1': 'admin@example.com',
            'email2': 'buyer@example.com',
            'email3': 'seller@example.com'
        }
    )
    session.commit()