from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def get_birthdays(db: AsyncSession, skip: int = 0, limit: int = 100):
    # Use select with joinedload to fetch reminders
    from sqlalchemy.orm import selectinload
    result = await db.execute(select(models.Birthday).options(selectinload(models.Birthday.reminders)).offset(skip).limit(limit))
    return result.scalars().all()

async def get_birthday(db: AsyncSession, birthday_id: int):
    from sqlalchemy.orm import selectinload
    result = await db.execute(select(models.Birthday).options(selectinload(models.Birthday.reminders)).filter(models.Birthday.id == birthday_id))
    return result.scalar_one_or_none()

async def create_birthday(db: AsyncSession, birthday: schemas.BirthdayCreate):
    # Create birthday
    db_birthday = models.Birthday(
        name=birthday.name,
        date=birthday.date,
        is_lunar=birthday.is_lunar,
        email=birthday.email,
        note=birthday.note
    )
    db.add(db_birthday)
    await db.commit()
    await db.refresh(db_birthday)
    
    # Create reminders
    for reminder in birthday.reminders:
        db_reminder = models.Reminder(
            birthday_id=db_birthday.id,
            days_before=reminder.days_before,
            time=reminder.time
        )
        db.add(db_reminder)
    
    await db.commit()
    await db.refresh(db_birthday)
    return db_birthday

async def delete_birthday(db: AsyncSession, birthday_id: int):
    birthday = await get_birthday(db, birthday_id)
    if birthday:
        await db.delete(birthday)
        await db.commit()
    return birthday

async def update_birthday(db: AsyncSession, birthday_id: int, birthday_data: schemas.BirthdayCreate):
    birthday = await get_birthday(db, birthday_id)
    if birthday:
        for key, value in birthday_data.dict().items():
            setattr(birthday, key, value)
        await db.commit()
        await db.refresh(birthday)
    return birthday
