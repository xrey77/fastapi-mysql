import os
from typing import Dict
from db import SessionLocal, engine
import model
from PIL import Image
from fastapi import FastAPI, Depends, File, UploadFile
from sqlalchemy.orm import Session
from model import Users

uploadpicture = FastAPI()

def connection():
    try:
        db = SessionLocal()
        yield db
        print("connected...")
    except:
        print("unable to connect...")
        db.close()

model.Base.metadata.create_all(bind=engine)


@uploadpicture.put("/uploaduserpicture/{id}")
def uploadPicture(id: str, file:  UploadFile = File(), db: Session = Depends(connection)) -> dict:
        
    img = Image.open(file.file)
    ext = "." + img.format

    MAX_SIZE = (100, 100) 
    img.thumbnail(MAX_SIZE)
    path =  "static/users/"
    newfile = "00"+id +  ext
    os.remove("static/users/00"+id+ext)

    final_filepath = os.path.join(path, newfile)
    img.save(final_filepath)
    urlimg ="http://127.0.0.1:8000/users/"+newfile
    user = db.query(Users).filter(Users.id == int(id)).first()
    if user:
        user.picture = urlimg
        db.commit()    
        return {"statusocde": 200, "message": "Successfully updated."}
    else:
        return {"statusocde":404, "message": "Unable to update user profile."}
    