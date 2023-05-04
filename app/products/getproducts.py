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
from sqlalchemy import desc
from model import Products
from schema import CreateAndUpdateUser
from app.hashing import Hasher
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

getproducts = FastAPI()

def connection():
    try:
        db = SessionLocal()
        yield db
        print("connected...")
    except:
        print("unable to connect...")
        db.close()

model.Base.metadata.create_all(bind=engine)


@getproducts.get("/getallproducts/{page}")
async def getproductlist(page: int, db: Session = Depends(connection)) -> dict:
    perpage = 10
    totalrecs = db.query(Products).count()
    
    # CALCULATE TOTAL PAGES
    totalpage = math.ceil(float(totalrecs) / perpage)
    offset = (page - 1) * perpage
    
    products = db.query(Products).offset(offset).limit(perpage).all()  #.order_by(Products.id.asc())
    return {"page": page,"totpages":totalpage,"products": products}    
    