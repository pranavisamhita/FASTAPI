from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
def login():
    return {"message": "Login endpoint working"}
