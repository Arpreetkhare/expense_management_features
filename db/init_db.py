from db.database import async_engine,Base
from api.auth.models import User
from api.expense.models import Expense
from api.group.models import GroupMember,user_groups,User



Base.metadata.create_all(bind=async_engine)