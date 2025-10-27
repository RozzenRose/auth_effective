from app.database.engine import Base
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    fathername = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    is_activate = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_seller = Column(Boolean, default=False)
    is_buyer = Column(Boolean, default=True)


    def to_dict(self):
        return {'id': self.id,
                'firstname': self.firstname,
                'fathername': self.fathername,
                'lastname': self.lastname,
                'username': self.username,
                'email': self.email,
                'hashed_password': self.hashed_password,
                'is_active': self.is_activate,
                'is_admin': self.is_admin,
                'is_seller': self.is_seller,
                'is_buyer': self.is_buyer}
