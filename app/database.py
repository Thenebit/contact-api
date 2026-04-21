import os
from sqlmodel import SQLModel, create_engine, Session

DB_USER = os.getenv("POSTGRES_USER", "contact")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "contact_dev_pw")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "contact_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
	SQLModel.metadata.create_all(engine)

def get_session():
	with Session(engine) as session:
		yield session
