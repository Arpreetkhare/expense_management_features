import uuid
from datetime import datetime


from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.group.schema import GroupCreate
from depends import __user_model
from api.auth.models import User
from .schema import GroupCreate,GroupMemberCreate,GroupMemberResponse,GroupResponse,GroupUpdate
from .models import user_groups,GroupMember


# Create group service function
async def create_group_service(request: GroupCreate, db: AsyncSession, token: str):
    try:
        # Retrieve the current user based on token
        current_user = __user_model(token)
        result = await db.execute(select(User).filter_by(user_id=current_user))
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
        
        # Create a new group
        new_group = user_groups(
            user_id=current_user,
            group_id=str(uuid.uuid4()), 
            group_name=request.group_name,
            description=request.description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_group)
        await db.commit()
        await db.refresh(new_group)
        
        return new_group

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "creds error"})

async def addMEMBER_service(group_id:str,request:GroupMemberCreate,db:AsyncSession,token:str):
    try:
        # Retrieve the current user based on token
        current_user = __user_model(token)
        result = await db.execute(select(User).filter_by(user_id=current_user))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
        
        group_res = await db.execute(select(user_groups).filter_by(group_id=group_id))
        group = group_res.scalars().first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        add_member=GroupMember(
          
            group_id=group_id,      
            user_id= request.user_id,
            role=request.role,
            joined_at = datetime.utcnow()

        )

        db.add(add_member)
        await db.commit()
        await db.refresh(add_member)
        
        return add_member
    

    except Exception as e:
        
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "creds error"})


async def getGroupMembers_service(group_id:str,request:GroupMemberCreate,db:AsyncSession,token:str):
    try:
        # Retrieve the current user based on token
        current_user = __user_model(token)
        result = await db.execute(select(User).filter_by(user_id=current_user))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
        
        group_res = await db.execute(select(GroupMember).filter_by(group_id=group_id))
        group_member = group_res.scalars().all()
        if not group_member:
            raise HTTPException(status_code=404, detail="Group members not found")
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "creds error"})    
        

        

async def getGroups_service(db:AsyncSession,token:str):
    try:
        current_user = __user_model(token)
        result = await db.execute(select(User).filter_by(user_id=current_user))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
        
        group_res = await db.execute(select(user_groups).filter_by(user_id=current_user))
        group = group_res.scalars().all()
        if not group:
            raise HTTPException(status_code=404, detail="no groups for this user")
        
        return group
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "creds error"})