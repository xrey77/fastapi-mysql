import time
from typing import Dict
import pyotp
import jwt
from decouple import config

from db import SessionLocal, engine
import schema
import model
from fastapi import FastAPI, Request, Response, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from model import Users
from schema import CreateAndUpdateUser
from app.hashing import Hasher
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse

register = FastAPI()

def connection():
    try:
        db = SessionLocal()
        yield db
        print("connected...")
    except:
        print("unable to connect...")
        db.close()

model.Base.metadata.create_all(bind=engine)

@register.post("/signup/")
async def signup(request: Request, db: Session = Depends(connection)) -> dict:
    data = await request.json()
    lname = data['lastname']
    fname = data['firstname']
    mail = data['email']
    mobile = data['mobile']
    usrname = data['username']
    pwd = data['password']
    hashpwd = Hasher.get_password_hash(pwd)
    secret = pyotp.random_base32()

    findEmail = db.query(Users).filter(Users.email == mail).first()
    if findEmail is not None:
        return {"statusocde": 200, "message": "Email Address has alredy taken."}    
    
    findUsername = db.query(Users).filter(Users.username == usrname).first()
    if findUsername is not None:
        return {"statusocde": 200, "message": "Username has alredy taken."}
    
    urlimg="http://127.0.0.1:8000/users/user.jpg"
    user = Users(lastname=lname, firstname=fname, email=mail, mobile=mobile, username=usrname, password=hashpwd, picture=urlimg, secretkey=secret)
    db.add(user)
    db.commit()    

    return {"statusocde": 200, "message": "You have registered successfully."}
    
