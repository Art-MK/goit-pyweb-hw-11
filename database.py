import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging_config

DATABASE_URL = "postgresql://postgres:postgres@localhost/FastAPI"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Check database connection
try:
    with engine.connect() as connection:
        logging.info("Successfully connected to the database.")
except Exception as e:
    logging.error(f"Error connecting to the database: {e}")
