from app.database.engine import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class AccessTokenBlackList(Base):
    __tablename__ = 'access_token_black_list'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, nullable=False)
    access_token = Column(String, nullable=False)

    user = relationship("User", back_populates='access_token', foreign_keys=[owner_id])


    def to_dict(self):
        return {'id': self.id,
                'owner_id': self.owner_id,
                'refresh_token': self.refresh_token}
