
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse

from app.auth.signin import login
from app.auth.signup import register
from app.auth.activateotp import otpactivate
from app.auth.validateotp import checkotp

from app.users.getuserbyid import getuser
from app.users.getusers import getusers
from app.users.updateuser import updateuser
from app.users.deleteuser import deluser
from app.users.uploadpicture import uploadpicture

from app.products.getproducts import getproducts
from app.products.getproductdetails import getproddetails
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/api/v1", login)
app.mount("/api/v2", register)
app.mount("/api/v10", otpactivate)
app.mount("/api/v11", checkotp)

app.mount("/api/v3", getuser)
app.mount("/api/v4", getusers)
app.mount("/api/v5", updateuser)
app.mount("/api/v6", deluser)
app.mount("/api/v9", uploadpicture)

app.mount("/api/v7", getproducts)
app.mount("/api/v8", getproddetails)


# templates = Jinja2Templates(directory="static")

@app.get("/")
async def serve_index(request: Request):    
    return RedirectResponse(url='/docs')    

@app.get("/images/{image}")
async def serve_image(image: str) -> dict:
    img = "static/images/"+image
    return FileResponse(img)

@app.get("/users/{image}")
async def serve_image(image: str) -> dict:
    img = "static/users/"+image
    return FileResponse(img)
                
@app.get("/products/{image}")
async def serve_image(image: str) -> dict:
    img = "static/products/"+image
    return FileResponse(img)
