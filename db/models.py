from sqlalchemy import Column, Integer, String
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    first_name = Column(String(50), nullable=True, )
    last_name = Column(String(50), nullable=True, )
    username = Column(String(50), nullable=True, )
