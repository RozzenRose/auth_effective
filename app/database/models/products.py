from app.database.engine import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

    user = relationship("User", back_populates='products', foreign_keys=[owner_id])

    def to_dict(self):
        return {'id': self.id,
                'owner_id': self.owner_id,
                'name': self.name,
                'description': self.description,
                'price': self.price}
