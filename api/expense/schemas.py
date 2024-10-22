from typing import Optional
from enum import Enum

from pydantic import BaseModel, validator

class ExpenseCategoryEnum(str, Enum):
    Food = 'Food'
    Transport = 'Transport'
    Shopping = 'Shopping'
    Entertainment = 'Entertainment'




class ExpenseModel(BaseModel):
    # user_id: str
    expense_name: str
    expense_category: Optional[ExpenseCategoryEnum] = ExpenseCategoryEnum.Food
    expense_tag: Optional[str] = None
    expense_amount: float
    
    class Config:
        orm_mode = True

class updateExpense(BaseModel):
    
    expense_name: str
    expense_category: Optional[ExpenseCategoryEnum] = ExpenseCategoryEnum.Food
    expense_tag: Optional[str] = None
    expense_amount: float
    
    class Config:
        orm_mode = True

       


class Settings(BaseModel):
    authjwt_secret_key: str = 'b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02'
