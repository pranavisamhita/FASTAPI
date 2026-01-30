from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI(
    title="Purview API",
    description="Admin-based API for Purview Digital",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
FAKE_TOKEN = "admin-token"

def authenticate_user(username: str, password: str):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)]):
    if token != FAKE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    return ADMIN_USERNAME

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Wrong username or password")

    return {
        "access_token": FAKE_TOKEN,
        "token_type": "bearer"
    }


class AdminData(BaseModel):
    title: str
    description: str

class AdminDataOut(AdminData):
    id: int

admin_data_db: List[AdminDataOut] = []

@app.get("/")
def root():
    return {"message": "Purview API is running"}

@app.get("/admin-data", response_model=List[AdminDataOut])
def get_all_data(admin: str = Depends(get_current_admin)):
    return admin_data_db

@app.post("/admin-data", response_model=AdminDataOut)
def create_data(data: AdminData, admin: str = Depends(get_current_admin)):
    new_item = AdminDataOut(
        id=len(admin_data_db) + 1,
        title=data.title,
        description=data.description
    )
    admin_data_db.append(new_item)
    return new_item

@app.put("/admin-data/{item_id}", response_model=AdminDataOut)
def update_data(item_id: int, data: AdminData, admin: str = Depends(get_current_admin)):
    for item in admin_data_db:
        if item.id == item_id:
            item.title = data.title
            item.description = data.description
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/admin-data/{item_id}")
def delete_data(item_id: int, admin: str = Depends(get_current_admin)):
    for item in admin_data_db:
        if item.id == item_id:
            admin_data_db.remove(item)
            return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

