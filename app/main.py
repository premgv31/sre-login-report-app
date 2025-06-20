import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta

# JWT settings
SECRET_KEY = "your-very-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI app instance
app = FastAPI()

# Resolve static path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount /static for style.css access
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve the index.html from static directory
@app.get("/")
def get_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# Dummy in-memory user database
USERS = {
    "admin": "password123"
}

# Request and token models
class LoginRequest(BaseModel):
    username: str
    password: str

# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decode and validate JWT token
def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in USERS:
            raise HTTPException(status_code=403, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

# Login API endpoint
@app.post("/login")
def login(req: LoginRequest):
    if USERS.get(req.username) == req.password:
        token = create_access_token({"sub": req.username})
        return {"message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Protected report endpoint
@app.get("/report")
def get_report(token: str):
    username = verify_token(token)
    return {"report": f"Hello {username}, here is your dummy report data."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
