from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta

# JWT settings
SECRET_KEY = "your-very-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Static HTML
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def get_index():
    return FileResponse("app/static/index.html")


# Dummy DB
USERS = {"admin": "password123"}


# Data models
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str | None = None


# Auth logic
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in USERS:
            raise HTTPException(status_code=403, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


# Endpoints
@app.post("/login")
def login(req: LoginRequest):
    if USERS.get(req.username) == req.password:
        token = create_access_token({"sub": req.username}, timedelta(minutes=30))
        return {"message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/report")
def get_report(token: str):
    username = verify_token(token)
    return {"report": f"Hello {username}, here is your dummy report data."}

