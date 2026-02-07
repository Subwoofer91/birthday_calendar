from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Birthday(Base):
    __tablename__ = "birthdays"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    is_lunar = Column(Boolean, default=False)
    email = Column(String, nullable=True)
    note = Column(String, nullable=True)

    reminders = relationship("Reminder", back_populates="birthday", cascade="all, delete-orphan")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    birthday_id = Column(Integer, ForeignKey("birthdays.id"))
    days_before = Column(Integer, default=0)
    time = Column(String, default="09:00") # HH:MM

    birthday = relationship("Birthday", back_populates="reminders")
