from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["Users"])

class UserProfile(BaseModel):
    name: str
    weight_lb: float
    height_in: float
    age: int
    gender: str
    goal: str
    dietary_preferences: str
    level: str  # beginner / intermediate / expert

@router.post("/create")
async def create_user(user: UserProfile):
    """Save user profile to database"""
    user_dict = user.dict()
    result = await db.users.insert_one(user_dict)
    return {"user_id": str(result.inserted_id)}

@router.get("/{user_id}")
async def get_user(user_id: str):
    """Fetch user profile by ID"""
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return user