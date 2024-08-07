from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.declarative import declarative_base



SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://dev:3306@localhost:3306/expense_management_features"  # Update with your database name

# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test_db"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = sessionmaker(
    # autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)
Base = declarative_base()
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            await session.close()


