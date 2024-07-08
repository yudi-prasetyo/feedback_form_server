from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseSettings
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")

settings = Settings()

if not settings.database_url:
    raise ValueError("No DATABASE_URL environment variable set")

engine = create_async_engine(settings.database_url, future=True, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
