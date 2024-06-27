import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

postgres_user = os.environ.get("POSTGRES_USER", "")
postgres_password = os.environ.get("POSTGRES_PASSWORD", "")
postgres_db= os.environ.get("POSTGRES_DB", "")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{postgres_user}:{postgres_password}@{postgres_db}:5432/{postgres_db}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()