import jwt
import datetime
from flask import request
from models import UserModel
from db import SessionLocal

SECRET_KEY = "B4l0nku@da5!"

def generate_token(user):
    payload = {
        "sub":user.id,
        "exp":datetime.datetime.utcnow()+datetime.timedelta(hours=2)
    }
    print(payload)
    return jwt.encode(payload, SECRET_KEY,algorithm="HS256")

def get_current_user():
    auth_header = request.headers.get("Authorization","")
    token = auth_header.replace("Bearer ","")
    try:
        payload = jwt.decode(token.strip('"'), SECRET_KEY, algorithms=["HS256"])
        user_id = payload["sub"]
        db = SessionLocal()
        return db.query(UserModel).filter(UserModel.id == user_id).first()
    except Exception as e:
        return None

def generate_refresh_token(user):
    payload = {
        "sub":user.id,
        "exp":datetime.datetime.utcnow()+datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY,algorithm="HS256")

def decode_refresh_token(refresh_token):
    return jwt.decode(refresh_token,SECRET_KEY,algorithms=["HS256"])
