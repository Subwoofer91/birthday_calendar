from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class ReminderBase(BaseModel):
    days_before: int
    time: str

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    birthday_id: int

    class Config:
        orm_mode = True

class BirthdayBase(BaseModel):
    name: str
    date: date
    is_lunar: bool = False
    email: Optional[str] = None
    note: Optional[str] = None

class BirthdayCreate(BirthdayBase):
    reminders: List[ReminderCreate] = []

class Birthday(BirthdayBase):
    id: int
    reminders: List[Reminder] = []

    class Config:
        orm_mode = True
