from fastapi  import  FastAPI, status, Response, Depends, HTTPException
from pydantic import  BaseModel
from dotenv import load_dotenv
from supabase import  create_client, Client
import os 

load_dotenv()

class Sign(BaseModel):
    email: str
    password: str 

app = FastAPI()

supbase: Client = create_client(os.getenv("SUP_URL"), os.getenv("SUP_KEY"))
print("Server running and connnected to Supabase")

@app.get("/")
async def root():
    """Return Server Status"""
    return {"Name" : "Auth Api","Status" : "Running", "Version": "1.0v"}



@app.post("/auth/signup", status_code=201)
async def  handleSignUp(signup: Sign):
    if not signup.email:
        raise HTTPException(status_code=400,  detail="Please include email")
    if not signup.password:
        raise HTTPException(status_code=400,  detail="Please inlclude password")
    
    try:
        response = supbase.auth.sign_up(
            {
                "email": f"{signup.email}",
                "password": f"{signup.password}",
            }
            )
    except:
        raise HTTPException(status_code=400, detail=f"Couldn't Sign up { signup.email }. Try again!.")
    return response

@app.post("/auth/login", status_code=200)
async def handleSignIn(login: Sign):
    if not login.email:
        raise HTTPException(status_code=400, detail="Please include email")
    
    if not login.password:
        raise HTTPException(status_code=400,  detail="Please inlclude password")

    try:
        response = supbase.auth.sign_in_with_password(
            {
                "email": f"{login.email}",
                "password": f"{login.password}",
            }
        )
    except:
            raise HTTPException(status_code=401, detail="Invalid Login crednetials!")

    return response
