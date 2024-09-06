from pydantic import BaseModel

from typing import Optional
from enum import Enum


class ExpenseCategoryEnum(str, Enum):
    Food = 'Food'
    Transport = 'Transport'
    Shopping = 'Shopping'
    Entertainment = 'Entertainment'




class ExpenseModel(BaseModel):
    user_id: str
    expense_name: str
    expense_category: Optional[ExpenseCategoryEnum] = ExpenseCategoryEnum.Food
    expense_tag: Optional[str] = None
    expense_amount: float
    
    class Config:
        orm_mode = True