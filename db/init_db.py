from db.database import async_engine,Base
from models import User,Expense


Base.metadata.create_all(bind=async_engine)