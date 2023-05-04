import math
import time
from typing import Dict

import jwt
from decouple import config

from db import SessionLocal, engine
import schema
import model
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from model import Products
from schema import CreateAndUpdateUser
from app.hashing import Hasher
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

getproddetails = FastAPI()

def connection():
    try:
        db = SessionLocal()
        yield db
        print("connected...")
    except:
        print("unable to connect...")
        db.close()

model.Base.metadata.create_all(bind=engine)


@getproddetails.get("/getproductdetails/{page}")
async def getproductlist(page: int, db: Session = Depends(connection)) -> dict:
    perpage = 10
    totalrecs = db.query(Products).count()
    
    # CALCULATE TOTAL PAGES
    totalpage = math.ceil(float(totalrecs) / perpage)
    offset = (page - 1) * perpage
    
    products = db.query(Products).offset(offset).limit(perpage).all()  #.order_by(Products.id.asc())
    return {"page": page,"totpages":totalpage,"products": products}    
    