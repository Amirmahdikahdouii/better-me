from sqlalchemy import Column, Integer, String, ForeignKey, Date, func, Text
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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserHabit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="habits")
    notes = relationship("HabitNote", back_populates="habit")
    start_date = Column(Date, default=func.current_date())

    def __repr__(self):
        return self.user.user_id

    def __str__(self):
        return self.name


class HabitNote(Base):
    __tablename__ = "habit_note"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    habit = relationship("UserHabit", back_populates="notes")
    title = Column(String(250), nullable=False)
    note = Column(Text, nullable=True)

    def __repr__(self):
        return self.habit.name

    def __str__(self):
        return self.habit.name
