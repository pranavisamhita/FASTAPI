from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

fake_user = {
    "username": "admin",
    "password": "admin123"
}

def authenticate_user(username: str, password: str):
    return username == fake_user["username"] and password == fake_user["password"]

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    if token != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token

@router.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Wrong username or password")

    return {
        "access_token": "admin",
        "token_type": "bearer"
    }
