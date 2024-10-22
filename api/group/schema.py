from datetime import datetime
from typing import Optional


from pydantic import BaseModel, validator




class GroupCreate(BaseModel):
    group_name: str  # Required field for creating a group
    description: Optional[str] = None  # Optional description of the group

class GroupUpdate(BaseModel):
    group_name: Optional[str] = None  # Allow updating of group name
    description: Optional[str] = None  # Allow updating of description

class GroupResponse(BaseModel):
    # user_id=str
    group_id: str  # ID of the group
    group_name: str  # Group name
    description: Optional[str] = None  # Description of the group
    created_at: datetime  # Timestamp of group creation
    updated_at: datetime  # Timestamp of the last update

    class Config:
        orm_mode = True 


class GroupMemberCreate(BaseModel):
     
    user_id: str  
    role: str  
class GroupMemberResponse(BaseModel):
    id: int
    group_id: str 
    user_id: str
    role: str 
    joined_at: datetime

    class Config:
        orm_mode = True 