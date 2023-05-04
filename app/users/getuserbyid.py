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

getuser = FastAPI()

def connection():
    try:
        db = SessionLocal()
        yield db
        print("connected...")
    except:
        print("unable to connect...")
        db.close()

model.Base.metadata.create_all(bind=engine)

def decodeJWT(token: str) -> dict:
    try:
        JWT_SECRET = config("secret")
        JWT_ALGORITHM = config("algorithm")                    
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
def verify_jwt(jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid        



@getuser.get("/getuserbyid/{id}")
async def getuserbyid(id, request: Request, db: Session = Depends(connection)) -> dict:
    usrmail = request.cookies.get("usermail")
    # print("USER MAIL : ",usrmail)
    try: 
        token = request.headers["Authorization"][7:]
        x1 = decodeJWT(token)
        if x1['user_id'] != usrmail:
            user = db.query(Users).filter(Users.id == id).first()
            if user:
                return {"statuscode": 200, "message": "", "user": user}
            else:
                return {"statusocde": 404, "message": "User ID not found."}
        else:
            return {"statusocde": 403, "message": "UnAuthorized Access."}
            
    except Exception as e:
        return {"statusocde": 401, "message": "Access Forbidden."}

    
    
