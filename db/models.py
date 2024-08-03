from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    first_name = Column(String(50), nullable=True, )
    last_name = Column(String(50), nullable=True, )
    username = Column(String(50), nullable=True, )
    state = Column(String(50), nullable=True, )
    habits = relationship("UserHabit", back_populates="user")

    def __repr__(self):
        return f"{self.id}. {self.user_id}"


class UserHabit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="habits")

    def __repr__(self):
        return self.user.user_id

