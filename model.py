from datetime import datetime, time, timedelta

# from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, TIMESTAMP

from db import Base
from datetime import datetime

class Users(Base):
    __tablename__ = "Users"    
    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String(20))
    firstname = Column(String(20))
    email = Column(String(20), unique=True)
    mobile = Column(String(20))
    username = Column(String(20), unique=True)
    password = Column(String(200))
    isactivated = Column(Integer, default=0, nullable=True)
    isblocked = Column(Integer, default=0, nullable=True)
    mailtoken = Column(Integer, default=0, nullable=True)
    secretkey = Column(Text())
    qrcodeurl = Column(Text())
    picture = Column(String(200))
    # created_at = Column(TIMESTAMP(), nullable=True)
    updated_at = Column(TIMESTAMP(), nullable=True)
    
class Products(Base):
    __tablename__ = "Products"    
    id = Column(Integer, primary_key=True, index=True)    
    descriptions = Column(String(255))
    qty = Column(Integer, default=0, nullable=True)
    unit = Column(String(20))
    cost_price = Column(Float)
    sell_price = Column(Float)
    prod_pic = Column(String(100))
    category = Column(String(20))
    sale_price = Column(Float)
    alert_level = Column(Integer, default=0, nullable=True)
    critical_level = Column(Integer, default=0, nullable=True)
    datecreated =Column(TIMESTAMP(), nullable=True)
    dateupdated = Column(TIMESTAMP(), nullable=True)
    
