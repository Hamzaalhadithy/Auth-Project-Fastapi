from fastapi  import  FastAPI, status, Response, Depends, HTTPException, Header, Depends
from pydantic import  BaseModel
from dotenv import load_dotenv
from typing import Annotated
from supabase import  create_client, Client
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os 

load_dotenv()

class Sign(BaseModel):
    email: str
    password: str 

app = FastAPI()


supbase: Client = create_client(os.getenv("SUP_URL"), os.getenv("SUP_KEY"))
print("Server running and connnected to Supabase")


cookie_schema = HTTPBearer(scheme_name="JWT", bearerFormat="Bearer <token>")
async def handleAuthentication(credentials: HTTPAuthorizationCredentials | None = Depends(cookie_schema)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Access token required")
    try:
        response = supbase.auth.get_user(credentials.credentials)
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return credentials.credentials
    
authenticatDep = Annotated[str, Depends(handleAuthentication)]


                           
@app.get("/")
async def root():
    """Return Server Status"""
    return {"Name" : "Auth Api","Status" : "Running", "Version": "1.0v"}

@app.get("/public/info")
async def handleInfo(response: Response):
    response.status_code = 200
    return {"message" : "Welcome Stranger! This info is public!."}


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


@app.post("/auth/logout", status_code=204)
async def handleLogout(authentication: authenticatDep):
    try:
        supbase.auth.sign_out()
    except:
        raise HTTPException(status_code=401, detail="Couldn't  Sign out. Try again!")
    return

@app.get("/protected/profile")
async def handleProfile(authentication: authenticatDep):
    
    return supbase.auth.get_user(authentication)

@app.get("/protected/dashboard")
async def handleDashboard(authentication:  authenticatDep):
    return {"message": "You have entered the dashboard info"}