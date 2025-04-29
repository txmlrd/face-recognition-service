from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import Config

# Step 1: Create engine and session
Base = declarative_base()

def init_db(app=None):
    database_url = f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}"
    engine = create_engine(database_url, pool_recycle=3600)  # Mengatur waktu recycle untuk connection pool
    Session = sessionmaker(bind=engine)
    return engine, Session
