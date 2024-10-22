from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from db.database import get_db
from api.expense.views import expense
from api.auth.views import generate_otp
from api.group.view import group


app=FastAPI()

@app.on_event("startup")
async def startup_event():
    async for db in get_db():
        await db.execute(text("select 1"))
        print("db connected")
        break

@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"message": "Connection to database successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error", headers={"Error": str(e)})

app.include_router(expense, tags=["expense"])
app.include_router(generate_otp,tags=['generate_otp'])
app.include_router(group,tags=['group'])










