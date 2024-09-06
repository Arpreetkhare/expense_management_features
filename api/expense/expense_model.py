from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType 
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey,Float, Enum,DateTime

class DBBase(DeclarativeBase):
    pass

class ExpenseCategoryEnum(str, enum.Enum):
    Food = "Food"
    Transport = "Transport"
    Shopping = "Shopping"
    Entertainment = "Entertainment"


class Expense(DBBase):
    __tablename__ = 'expense'
    expense_id: Mapped[str] = mapped_column(String(500), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(500), ForeignKey('user.user_id'))
    expense_name:Mapped[str] = mapped_column(String(225), nullable=False)
    expense_category: Mapped[ExpenseCategoryEnum] = mapped_column(Enum(ExpenseCategoryEnum), nullable=False)
    expense_tag:Mapped[str] = mapped_column(String(225), nullable=True)
    expense_amount:Mapped[str] = mapped_column(Float, nullable=False)
    created_at:Mapped[str] = mapped_column(Integer)
    updated_at:Mapped[str] = mapped_column(Integer)  







    




