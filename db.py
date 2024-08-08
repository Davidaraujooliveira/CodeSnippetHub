from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import sys
from alembic import command
from alembic.config import Config


def setup_alembic_config(engine_url):
    """
    Set up and return the Alembic configuration.
    """
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", engine_url)
    return alembic_cfg


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

# Setup Alembic configuration and run migrations automatically
alembic_cfg = setup_alembic_config(DATABASE_URL)
try:
    command.upgrade(alembic_cfg, "head")
except Exception as e:
    sys.exit(f"Failed to run Alembic migrations: {e}")