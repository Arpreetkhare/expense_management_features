import uuid
from datetime import datetime,timedelta

from fastapi import HTTPException, status
from fastapi import APIRouter,Depends,status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update,func



from .models import Expense
from api.auth.models import User
from .schemas import ExpenseModel,updateExpense
from dependencies import AuthValidator
from depends import __user_model
from db.database import get_db


expense=APIRouter()


@expense.get("/get", status_code=status.HTTP_201_CREATED)

async def get_user(db: AsyncSession=Depends(get_db),token:str = Depends(AuthValidator())):
    try:
        current_user = __user_model(token)
       
        user = await db.execute(select(User).filter_by(user_id=current_user))
        user = user.scalars().first()
        if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token") 
    

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
            user_id=current_user,
            expense_id=str(uuid.uuid4()),
            expense_name=request.expense_name,
            expense_category=request.expense_category,
            expense_amount=request.expense_amount,
            expense_tag=request.expense_tag,
            created_at=datetime.now(),  
            updated_at=datetime.now() 
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


@expense.get("/get_expense", status_code=status.HTTP_200_OK)
async def get_expense(db: AsyncSession = Depends(get_db), token: str = Depends(AuthValidator())):
    try:
        # Get the authenticated user's ID from the token
        current_user = __user_model(token)

        # Fetch the user associated with the token
        user = await db.execute(select(User).filter_by(user_id=current_user))
        user = user.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})

        # Fetch the expenses for the authenticated user
        expense_result = await db.execute(select(Expense).filter_by(user_id=current_user))
        expenses = expense_result.scalars().all()

        if not expenses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "No expenses found for this user"})

        return expenses

    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "An error occurred while fetching expenses"})


@expense.put('/update_expense/{expense_id}',status_code=status.HTTP_201_CREATED)  
async def update_expense(expense_id:str,request:updateExpense,db:AsyncSession=Depends(get_db),token:str=Depends(AuthValidator())): 
    try:
        current_user = __user_model(token)
        user= await db.execute(select(User).filter_by(user_id=current_user))
        user = user.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
        

        expense_result = await db.execute(select(Expense).filter_by(expense_id=expense_id,user_id=current_user))
        expense = expense_result.scalars().first()
        if not expense:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Expense not found"} )
        

        update_expense= Expense( 
            user_id=current_user,
            expense_id=str(uuid.uuid4()),  # Generate a unique expense_id
            expense_name=request.expense_name,
            expense_category=request.expense_category,
            expense_amount=request.expense_amount,
            expense_tag=request.expense_tag,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
                    

        )
        db.add(update_expense)
        await db.commit()
        return update_expense
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": f"creds error"})





@expense.get('/monthly_report',status_code=status.HTTP_201_CREATED)  
async def monthly_report(db:AsyncSession=Depends(get_db),token:str=Depends(AuthValidator())): 
    try:
        current_user = __user_model(token)
        user= await db.execute(select(User).filter_by(user_id=current_user))
        user = user.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
        

        current_time = datetime.utcnow()
        interval= current_time - timedelta(days=30)
        report= await db.execute(
            select(Expense). where (Expense.created_at >= interval,  Expense.user_id == user.user_id)
            )
        report=report.scalars().all()

        return { "report":report}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": f"creds error"})





@expense.get('/monthly_expenses', status_code=status.HTTP_201_CREATED)
async def monthly_expenses(
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(AuthValidator())
): 
    try:
        current_user = __user_model(token)
        user = await db.execute(select(User).filter_by(user_id=current_user))
        user = user.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})

        # Get current time and interval of 30 days
        current_time = datetime.utcnow()
        interval = current_time - timedelta(days=30)

        # Query to get category-wise total of expenses
        report = await db.execute(
            select(
                Expense.expense_category, 
                func.sum(Expense.expense_amount).label('total_amount')
            )
            .where(Expense.created_at >= interval, Expense.user_id == user.user_id)
            .group_by(Expense.expense_category)
        )

        # Fetch all results
        report = report.all()

        # Format the report to be more user-friendly
        formatted_report = {
            category: total_amount for category, total_amount in report
        }

        return {"report": formatted_report}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "creds error"})



