from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, database, utils, models
from datetime import date, timedelta
import asyncio

scheduler = AsyncIOScheduler()

from datetime import datetime

async def check_birthdays():
    print("Checking birthdays...")
    async with database.SessionLocal() as db:
        birthdays = await crud.get_birthdays(db, limit=1000)
        now = datetime.now()
        current_time_str = now.strftime("%H:%M")
        today_date = now.date()
        
        for bday in birthdays:
            next_bday = utils.calculate_next_birthday(bday)
            days_left = (next_bday - today_date).days
            
            for reminder in bday.reminders:
                # Check if days match
                if days_left == reminder.days_before:
                    # Check if time matches (simple string comparison for now)
                    if current_time_str == reminder.time:
                        utils.send_notification(bday, days_left)

def start_scheduler():
    scheduler.add_job(check_birthdays, 'interval', minutes=1) # Run every minute
    scheduler.start()
