from fastapi import APIRouter,Depends,status

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import AuthValidator
from .schema import GroupCreate,GroupMemberCreate,GroupMemberResponse,GroupResponse,GroupUpdate
from .services import create_group_service,addMEMBER_service,getGroups_service
from db.database import get_db



group=APIRouter()

@group.post("/create_group", status_code=status.HTTP_201_CREATED, response_model=GroupResponse)
async def create_group(request: GroupCreate, db: AsyncSession = Depends(get_db), token: str = Depends(AuthValidator())):
    return await create_group_service(request, db, token)

@group.post('/add_member/{group_id}',status_code=status.HTTP_201_CREATED,response_model=GroupMemberResponse)
async def add_member(group_id:str,request: GroupMemberCreate, db: AsyncSession = Depends(get_db), token:str = Depends(AuthValidator())):
       return await addMEMBER_service(group_id,request,db,token)              

@group.get("/get_groups", status_code=status.HTTP_200_OK)
async def get_groups(db: AsyncSession = Depends(get_db), token: str = Depends(AuthValidator())):
    return await getGroups_service(db, token)
   


# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI4ZTFkZDgzNi1hMDllLTRiOTctYWE2ZS1kNWQ1NTU5NDU5YWYiLCJleHAiOjE3NTQwNzQ5NjZ9.45FPwfdc7qjfn_-hGjD4aKOLs_2GLg4b_aINOHTzJ8E