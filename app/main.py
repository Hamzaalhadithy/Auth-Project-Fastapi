from fastapi  import  FastAPI, status, Response, Depends, HTTPException
from pydantic import  BaseModel
from dotenv import load_dotenv
from supabase import  create_client, Client
import os 

load_dotenv()

app = FastAPI()

Client = create_client(os.getenv("SUP_URL"), os.getenv("SUP_KEY"))
print("Server running and connnected to Supabase")

@app.get("/")
async def root():
    """Return Server Status"""
    return {"Name" : "Auth Api","Status" : "Running", "Version": "1.0v"}

