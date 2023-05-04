import time
from typing import Dict

import jwt
from decouple import config

from db import SessionLocal, engine
import model 
import pyotp
from fastapi import FastAPI, Request, Response, Depends
from sqlalchemy.orm import Session
from model import Users

checkotp = FastAPI()

def connection():
    try:
        db = SessionLocal()
        yield db
        print("connected...")
    except:
        print("unable to connect...")
        db.close()

model.Base.metadata.create_all(bind=engine)

@checkotp.post("/validateotpcode")
async def checkotpcode(request: Request, db: Session = Depends(connection)):
    xdata = await request.json()
    mail = xdata['email']
    otp = int(xdata['otpcode'])
    try:    
        user = db.query(Users).filter(Users.email == mail).first()
        if user.secretkey:
            token = otp
            totp = pyotp.TOTP(user.secretkey)
            isOk = totp.verify(token)        
            if isOk:
                return {'statuscode': 200, 'message': 'OTP Code valid.','username': user.username}
            else:        
                return {'statuscode': 404, 'message': 'OTP Code not valid.'}
    except:
        return {'statuscode': 404, 'message': 'OTP Code not valid.'}
        