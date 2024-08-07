from fastapi.exceptions import HTTPException
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter,Depends,status
from fastapi_jwt_auth import AuthJWT
from models import User
# from depends import create_access_token,verify_password,verify_token,get_passwod_hash
# from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta
from passlib.context import CryptContext
from models import User
from schemas import UserModel
from api.otp_router import get_otp

SECRET_KEY = "b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02"
ALGORITHM = "AK1812"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

access_router=APIRouter()

@access_router.post('/login', status_code=status.HTTP_302_FOUND)
async def login(request:UserModel= Depends(), db: AsyncSession = Depends(get_db)):
    query = (
            select(User)
            .where(User.email == request.email)
        )
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    otp = get_otp()
    hash_otp = pwd_context.hash(str(otp))
    user.otp = hash_otp
    user.otp_expire = datetime.utcnow() + timedelta(minutes=5)
        
    db.add(user)
    await db.commit()
    await db.refresh(user)
        
        # Send OTP to user via email/SMS (omitted for brevity)
    print(f"OTP for user {user.first_name}: {otp}")  # Print OTP for demonstration
        
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="OTP sent to your email/SMS")

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(data={"sub": user.username}, expire_delta=access_token_expires)
    
    # return {"access_token": access_token, "token_type": "bearer"}

    

# @auth.post('/otp',status_code=status.HTTP_201_CREATED) 
# async def otp(request:User,db: AsyncSession=Depends(get_db)):

    
    

    