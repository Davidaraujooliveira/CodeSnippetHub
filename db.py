from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import sys

try:
    load_dotenv()
except Exception as e:
    sys.exit(f"Failed to load environment variables: {e}")

try:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
except Exception as e:
    sys.exit(f"Failed to read DATABASE_URL: {e}")

try:
    engine = create_engine(DATABASE_URL, echo=True, future=True)
except exc.SQLAlchemyError as e:
    sys.exit(f"Failed to create engine: {e}")
except Exception as e:
    sys.exit(f"An unexpected error occurred while creating the engine: {e}")

try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    sys.exit(f"Failed to create a SessionLocal instance: {e}")