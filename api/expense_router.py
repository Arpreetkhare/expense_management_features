import uuid
from fastapi import HTTPException, status
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session
# from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter,Depends,status
from fastapi_jwt_auth import AuthJWT
from models import Expense,User
from schemas import ExpenseModel
# from api.utils import authorize_user
from sqlalchemy import select
from datetime import datetime
from dependencies import AuthValidator
from depends import __user_model

expense=APIRouter()


@expense.get("/get", status_code=status.HTTP_201_CREATED)

async def get_user(user_id:str,db: AsyncSession=Depends(get_db)):
    try:
        

        query=select(User).where(User.user_id==user_id)
        result=await db.execute(query)
        expense=result.scalars().all()
        return expense
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token") from e
    

@expense.post("/add", dependencies=[Depends(AuthValidator())], status_code=status.HTTP_201_CREATED)
async def add_expense(request: ExpenseModel, db: AsyncSession = Depends(get_db), token:str = Depends(AuthValidator())):
    try:
        # Authorize.jwt_required()
        # The current user ID from the JWT token

        current_user = __user_model(token)
       
        user = await db.execute(select(User).filter_by(user_id=current_user))
        user = user.scalars().first()
        if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        

        new_expense = Expense(
            user_id=request.user_id,
            expense_id=str(uuid.uuid4()),
            expense_name=request.expense_name,
            expense_category=request.expense_category,
            expense_amount=request.expense_amount,
            expense_tag=request.expense_tag,
            created_at=int(datetime.now().timestamp()),
            updated_at=int(datetime.now().timestamp())
        )
        db.add(new_expense)
        await db.commit()
        return new_expense
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Error in router: {ex}"}
        )


@expense.get("/get_expense/{user_id}",status_code=status.HTTP_200_OK)
async def get_expense(user_id:str,db: AsyncSession=Depends(get_db), token:str = Depends(AuthValidator())):
    try:
        
        current_user = __user_model(token)
       
        user = await db.execute(select(User).filter_by(user_id=current_user))
        user = user.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})

        # Fetch the expenses for the user
        expense_result = await db.execute(select(Expense).filter_by(user_id=user_id))
        expenses = expense_result.scalars().all()

        if not expenses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "no expense with this user_id"})
        return expenses
    
    
        
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": f"expense not found"})


        