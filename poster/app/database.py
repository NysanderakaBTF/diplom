from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

from config import Config

# Database setup
engine = create_engine(Config.DJANGO_DATABASE_URI, echo=Config.DEBUG)
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

# Reflect Django app's tables
metadata = MetaData(bind=engine)
metadata.reflect()

# Map Django app's models
Post = metadata.tables['posts_post']  # Replace with your Django app's table name
Image = metadata.tables['posts_image']# Replace with your Django app's table name
Token = metadata.tables['socialaccount_socialtoken']
# Context manager for database sessions
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()