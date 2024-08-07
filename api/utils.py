# from fastapi import HTTPException, Depends, status
# from fastapi_jwt_auth import AuthJWT
# from models import User
# from sqlalchemy.ext.asyncio import AsyncSession
# from db.database import get_db
# from sqlalchemy import select

# async def get_current_user(db: AsyncSession = Depends(get_db), Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#         user_id = Authorize.get_jwt_subject()  # Extract user ID from the token
#         query = select(User).where(User.user_id == user_id)
#         result = await db.execute(query)
#         user = result.scalars().one_or_none()
#         if user is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
#         return user
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

# async def authorize_user(user_id: str, db: AsyncSession = Depends(get_db), Authorize: AuthJWT = Depends()):
#     user = await get_current_user(db=db, Authorize=Authorize)
#     if user.user_id != user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
