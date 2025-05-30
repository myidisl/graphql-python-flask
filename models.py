from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    refresh_token = Column(String, nullable=True)
    role = Column(String,default='user')
