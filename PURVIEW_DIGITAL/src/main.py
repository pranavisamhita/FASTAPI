from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Annotated

app = FastAPI(
    title="Purview API",
    description="Backend API for Purview Digital",
    version="1.0.0"
)


# ---------- DATABASE (SQLite) ----------
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

# ---------- AUTH ----------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# fake user (for testing)
fake_user = {
    "username": "admin",
    "password": "admin123"
}

def authenticate_user(username: str, password: str):
    if username == fake_user["username"] and password == fake_user["password"]:
        return True
    return False

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    if token != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token

# ---------- ROUTES ----------
@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    is_valid = authenticate_user(form_data.username, form_data.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Wrong username or password")

    return {
        "access_token": "admin",
        "token_type": "bearer"
    }

@app.get("/")
def root():
    return {"message": "API is working"}

@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": "You are authenticated"}


@app.get("/purview")
def purview_home(current_user: str = Depends(get_current_user)):
    return {
        "app": "Purview API",
        "status": "Authenticated access granted"
    }
