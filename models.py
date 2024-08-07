import enum
from typing import Literal
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
# from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey,Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType 
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey,Float, Enum,DateTime

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




category_enum = Literal['Food', 'Transport', 'Shopping', 'Entertainment' ]

class Expense(DBBase):
    __tablename__ = 'expense'
    expense_id: Mapped[str] = mapped_column(String(500), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(500), ForeignKey('user.user_id'))
    expense_name:Mapped[str] = mapped_column(String(225), nullable=False)
    expense_category:Mapped[category_enum] = mapped_column(Enum)
    expense_tag:Mapped[str] = mapped_column(String(225), nullable=True)
    expense_amount:Mapped[str] = mapped_column(Float, nullable=False)
    created_at:Mapped[str] = mapped_column(Integer)
    updated_at:Mapped[str] = mapped_column(Integer)  







    




