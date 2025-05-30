from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///data.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

#Buat tabel jika belum ada
def init_db():
    Base.metadata.create_all(bind=engine)