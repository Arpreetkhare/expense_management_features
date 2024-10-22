from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer,DateTime

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