from fastapi import APIRouter, Depends
from authentication.router import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users(current_user: str = Depends(get_current_user)):
    return ["User 1", "User 2"]

@router.post("/")
def create_user(current_user: str = Depends(get_current_user)):
    return {"message": "User created"}

@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: str = Depends(get_current_user)):
    return {"message": f"User {user_id} deleted"}
