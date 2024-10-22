import random
import uuid
from datetime import datetime, timedelta


from fastapi.exceptions import HTTPException
from fastapi import APIRouter,Depends,status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from passlib.context import CryptContext


from db.database import get_db
from .models import User
from depends import create_access_token,verify_token
from .schemas import SignupRequest, otpVali,otpVar


generate_otp=APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@generate_otp.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Check if user already exists
        existing_user = await db.execute(select(User).where(User.mobile_number == request.mobile_number))
        existing_user = existing_user.scalars().one_or_none()

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists with this mobile number")

        # Create a new user
        new_user = User(
            user_id=str(uuid.uuid4()),
            first_name=request.first_name,
            last_name=request.last_name,
            mobile_number=request.mobile_number,
            email=request.email
        )
        
        db.add(new_user)
        await db.commit()

        # Optionally, you can generate and send OTP here or in a separate endpoint
        return {"msg": "User registered successfully. You can now request an OTP."}
    
    except Exception as e:
        await db.rollback()
        print(e)
        raise HTTPException(status_code=400, detail=f"Error in registration: {str(e)}")

def get_otp():
    otp = random.randint(1000, 9999)
    return str(otp)

@generate_otp.post('/otp',status_code=status.HTTP_201_CREATED) 
async def create_otp(request: otpVali, db: AsyncSession = Depends(get_db)) :
    try:
        query = (
            select(User)
            .where(User.mobile_number == request.mobile_number)
        )

        result = await db.execute(query)
        user = result.scalars().one_or_none()
        

        if user is None :
            user = User(
                user_id = str(uuid.uuid4()),
                mobile_number=request.mobile_number,
            )
            db.add(user)
        
        otp=get_otp()

        hash_otp=pwd_context.hash(str(otp))
        otp_expire=datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)

        query = (
            update(User).where(User.mobile_number==request.mobile_number).values(otp=hash_otp,otp_expire=otp_expire)  
        )
        # print(query)
        await db.execute(query)
        await db.commit()

        # user.otp_expire =datetime.utcnow() + timedelta(minutes=5)

        return {"msg": "otp sent succesfully","otp":otp}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"error in router{e}")

@generate_otp.post('/verify-otp', status_code=status.HTTP_200_OK)
async def verify_otp(request:otpVar, db: AsyncSession = Depends(get_db)):
    try:

        query=(
            select(User)
            .where(User.mobile_number == request.mobile_number)
        )

        result=await db.execute(query)
        user=result.scalars().one_or_none()

        if user is None :
            raise HTTPException(status_code=400, detail="Invalid Credentials")
        

        if not pwd_context.verify(str(request.otp), user.otp):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
        

        if user.otp_expire < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP Expired")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.user_id}, expire_delta=access_token_expires)

        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error in OTP verification: {str(e)}")
    





        





