from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
# from schemas import Settings
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
# from models import Expense
# from fastapi_jwt_auth import AuthJWT

from db.database import get_db
from fastapi.exceptions import HTTPException
from api.expense_router import expense
# from api.auth_router import access_router
from api.otp_router import generate_otp
from api.auth_router import access_router

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
app.include_router(access_router,tags=['access_router'])
app.include_router(generate_otp,tags=['generate_otp'])


# @AuthJWT.load_config
# def get_config():
#     return Settings()








