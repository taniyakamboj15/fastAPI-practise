from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session
from app.core.config import settings

# Create the Database Engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    pool_pre_ping=True,
    echo=False
)

# Create a Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

