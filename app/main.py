from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

app = FastAPI()

# Dummy in-memory user data
USERS = {"admin": "password123"}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    if USERS.get(req.username) == req.password:
        return {"message": "Login successful", "token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/report")
def fetch_report(token: str = ""):
    if token != "fake-jwt-token":
        raise HTTPException(status_code=403, detail="Unauthorized")
    return {"report": "This is your dummy report data."}
