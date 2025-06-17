from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

# Mount static folder for serving HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_index():
    html_path = Path("static/index.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)

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

