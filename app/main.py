from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, database, crud, schemas, utils, scheduler
from datetime import date

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    scheduler.start_scheduler()

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: AsyncSession = Depends(database.get_db)):
    birthdays = await crud.get_birthdays(db)
    
    # Enrich data with next birthday and days left
    display_data = []
    today = date.today()
    for b in birthdays:
        next_bday = utils.calculate_next_birthday(b)
        days_left = (next_bday - today).days
        display_data.append({
            "id": b.id,
            "name": b.name,
            "date": b.date,
            "is_lunar": b.is_lunar,
            "next_birthday": next_bday,
            "days_left": days_left,
            "note": b.note,
            "email": b.email,
            "reminders": b.reminders # Pass reminders to template
        })
    
    # Sort by days left
    display_data.sort(key=lambda x: x["days_left"])

    return templates.TemplateResponse("index.html", {"request": request, "birthdays": display_data})

@app.post("/add")
async def add_birthday(
    request: Request,
    name: str = Form(...),
    date_str: str = Form(...),
    is_lunar: bool = Form(False),
    email: str = Form(None),
    note: str = Form(None),
    db: AsyncSession = Depends(database.get_db)
):
    # Parse reminders manually from form data because FastAPI Form doesn't support complex lists easily
    form_data = await request.form()
    reminders_days = form_data.getlist("reminders_days[]")
    reminders_time = form_data.getlist("reminders_time[]")
    
    reminders = []
    for d, t in zip(reminders_days, reminders_time):
        reminders.append(schemas.ReminderCreate(days_before=int(d), time=t))

    birth_date = date.fromisoformat(date_str)
    birthday_data = schemas.BirthdayCreate(
        name=name,
        date=birth_date,
        is_lunar=is_lunar,
        email=email,
        note=note,
        reminders=reminders
    )
    await crud.create_birthday(db, birthday_data)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{id}")
async def delete_birthday(id: int, db: AsyncSession = Depends(database.get_db)):
    await crud.delete_birthday(db, id)
    return RedirectResponse(url="/", status_code=303)
