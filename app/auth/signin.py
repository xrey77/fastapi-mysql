import time
from typing import Dict

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

login = FastAPI()

def connection():
    try:
        db = SessionLocal()
        yield db
        print("connected...")
    except:
        print("unable to connect...")
        db.close()

model.Base.metadata.create_all(bind=engine)


@login.post("/signin/")
async def signin(request: Request, response: Response, db: Session = Depends(connection)) -> dict:
    data = await request.json()
    usrname = data['username']
    pwd = data['password']
    findUsername = db.query(Users).filter(Users.username == usrname).first()
    if findUsername:
        response.set_cookie("usermail",findUsername.email, expires=8)
        if Hasher.verify_password(pwd, findUsername.password):
            
            payload = {
                "user_id": findUsername.email,
                "expires": time.time() + 28800000
            }
            JWT_SECRET = config("secret")
            JWT_ALGORITHM = config("algorithm")            
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
                   
            return {
                "statuscode": 200,
                "message": "Login successsful, please wait.",
                "userid": findUsername.id,
                "email": findUsername.email,
                "firstname": findUsername.firstname,
                "lastname": findUsername.lastname,
                "picture": findUsername.picture,
                "isactive": findUsername.isactivated,
                "isblocked": findUsername.isblocked,
                "username": findUsername.username,                
                "qrcodeurl": findUsername.qrcodeurl,
                "token": token}
        else:
            return {"statusocde": 404, "message": "Invalid password, please try again."}    
    else:
        return {"statusocde": 404, "message": "Username not found, please register."}    
                