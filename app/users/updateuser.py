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

updateuser = FastAPI()

def connection():
    try:
        db = SessionLocal()
        yield db
        print("connected...")
    except:
        print("unable to connect...")
        db.close()

model.Base.metadata.create_all(bind=engine)


@updateuser.put("/updateuser/{id}")
async def updateuserbyid(id: int, request: Request, db: Session = Depends(connection)) -> dict:
    data = await request.json()
    fname = data["firstname"]
    lname = data["lastname"]
    # pwd = data["password"]

    user = db.query(Users).filter(Users.id == id).first()
    if user:
        user.lastname = lname
        user.firstname = fname    
        db.commit()    
        return {"statusocde": 200, "message": "Successfully updated."}
    else:
        return {"statusocde": 404, "message": "Unable to update user profile."}
            