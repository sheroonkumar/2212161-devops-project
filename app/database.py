import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# It reads the connection string from Docker, or defaults to a local one
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgrespassword@localhost:5432/devops_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# This function yields a database session and safely closes it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()