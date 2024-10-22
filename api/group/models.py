from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey,DateTime, UniqueConstraint, func



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
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Use DateTime

class user_groups(DBBase):
    __tablename__ = 'user_groups'
    group_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    group_name:Mapped[str] = mapped_column(String, nullable=False)
    user_id:Mapped[str] = mapped_column(String(500), ForeignKey('user.user_id')) 
    description:Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Use DateTime


class GroupMember(DBBase):
    __tablename__ = 'group_members'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[str] = mapped_column(ForeignKey('user_groups.group_id'))
    user_id: Mapped[str] = mapped_column(ForeignKey('user.user_id'))  
    role: Mapped[str] = mapped_column(String(50))  
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('group_id', 'user_id', name='_group_user_uc'),)
    

