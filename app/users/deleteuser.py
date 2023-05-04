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
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse

deluser = FastAPI()

def connection():
    try:
        db = SessionLocal()
        yield db
        print("connected...")
    except:
        print("unable to connect...")
        db.close()

model.Base.metadata.create_all(bind=engine)


@deluser.delete("/deleteuser/{id}")
async def getuserbyid(id: int,request: Request, db: Session = Depends(connection)) -> dict:
   try:
      db.query(Users).filter(Users.id == id).delete()
      db.commit()
      return {"statusocde": 200, "message": "Delete successfully."}      
   except Exception as e:
        return {"statuscode": 404, "message": e}
    