from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

# GET
@router.get("/")
def get_users():
    return {"message": "Get all users"}

# POST
@router.post("/")
def create_user():
    return {"message": "User created"}

# PUT
@router.put("/{user_id}")
def update_user(user_id: int):
    return {"message": f"User {user_id} updated"}

# DELETE
@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted"}
