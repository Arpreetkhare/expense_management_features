from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey,Float, Enum,DateTime, func




class DBBase(DeclarativeBase):
    pass


class User(DBBase):
    __tablename__ = 'user'
    user_id: Mapped[str] = mapped_column(String(500), primary_key=True)
    first_name:Mapped[str] = mapped_column(String, nullable=False)
    last_name:Mapped[str] = mapped_column(String, nullable=False)
    mobile_number:Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email:Mapped[str] = mapped_column(String, nullable=False, unique=True)
    otp:Mapped[str] = mapped_column(String(60))
    otp_expire: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    created_at:Mapped[int] = mapped_column(Integer)
    updated_at:Mapped[int] = mapped_column(Integer)

# Define the SQLAlchemy Enum type correctly
category_enum = ('Food', 'Transport', 'Shopping', 'Entertainment')

class Expense(DBBase):
    __tablename__ = 'expense'
    
    expense_id: Mapped[str] = mapped_column(String(500), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(500), ForeignKey('user.user_id'))
    expense_name: Mapped[str] = mapped_column(String(225), nullable=False)
    
    # Use Enum for the expense_category field
    expense_category: Mapped[str] = mapped_column(Enum(*category_enum, name="expense_category_enum"), nullable=False)
    
    expense_tag: Mapped[str] = mapped_column(String(225), nullable=True)
    expense_amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())  # Automatically set current time
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now())






