import time
from typing import Dict

import jwt
from decouple import config

from db import SessionLocal, engine
import schema
import model
import pyotp
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

otpactivate = FastAPI()

def connection():
    try:
        db = SessionLocal()
        yield db
        print("connected...")
    except:
        print("unable to connect...")
        db.close()

model.Base.metadata.create_all(bind=engine)


@otpactivate.put("/activateotp/{id}")
async def activateTOTP(id: int, request: Request, db: Session = Depends(connection)) -> dict:
    data = await request.json()
    isOTPactivated = data["isactivated"]

    user = db.query(Users).filter(Users.id == id).first()
    if user:
        if isOTPactivated == "Y":
            TOTPSECRETKEY = user.secretkey
            fullname = user.firstname + " " + user.lastname
            qrcode = pyotp.totp.TOTP(TOTPSECRETKEY).provisioning_uri(name=fullname, issuer_name="DOHA BANK")
            user.qrcodeurl = qrcode
            db.commit()    
            return {"statusocde": 200, "message": "2FA has been Enabled."}
        else:
            user.qrcodeurl = None
            db.commit()    
            return {"statusocde": 404, "message": "2FA has been Disabled."}            
    else:
        return {"statusocde": 404, "message": "Unable to update user profile."}
            