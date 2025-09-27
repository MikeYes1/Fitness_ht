# routers/workout.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import random
from database import db
from bson import ObjectId

router = APIRouter(prefix="/workout", tags=["Workout"])

# ------------------------
# Request body model
# ------------------------
class WorkoutRequest(BaseModel):
    user_id: str  # only user_id needed now

# ------------------------
# Pools of exercises per body part
# ------------------------
exercise_pool = {
    "chest": ["Push-ups", "Bench Press", "Incline Bench Press", "Chest Fly", "Cable Crossovers", "Dumbbell Pullover"],
    "back": ["Pull-ups", "Lat Pulldown", "Bent-over Rows", "Seated Cable Row", "T-bar Row", "Superman"],
    "legs": ["Squats", "Lunges", "Leg Press", "Leg Curl", "Calf Raises", "Step-ups"],
    "abs": ["Plank", "Crunches", "Leg Raises", "Bicycle Crunch", "Mountain Climbers", "Russian Twists"],
    "arms": ["Bicep Curls", "Tricep Dips", "Hammer Curls", "Tricep Kickbacks", "Chin-ups", "Close Grip Push-ups"],
    "shoulders": ["Shoulder Press", "Lateral Raises", "Front Raises", "Upright Row", "Arnold Press", "Shrugs"],
    "cardio": ["Jump Rope", "Burpees", "Running", "Cycling", "High Knees", "Jumping Jacks"]
}

# ------------------------
# Helper functions
# ------------------------
async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def select_exercises(body_part: str, count: int = 3) -> List[str]:
    selected = random.sample(exercise_pool.get(body_part, []), min(count, len(exercise_pool.get(body_part, []))))
    detailed = []
    for ex in selected:
        if body_part == "cardio":
            detailed.append(f"{ex} – 20–30 minutes")
        elif body_part == "abs":
            detailed.append(f"{ex} – 3 sets × 20 reps")
        else:
            detailed.append(f"{ex} – 3 sets × 10–12 reps")
    return detailed

def generate_weekly_plan(plan_type: str) -> Dict[str, List[str]]:
    if plan_type == "starter":
        return {
            "Monday": select_exercises("chest"),
            "Tuesday": select_exercises("back"),
            "Wednesday": ["Rest / Active recovery (stretching, yoga, light walk)"],
            "Thursday": select_exercises("legs"),
            "Friday": select_exercises("arms"),
            "Saturday": ["Rest"],
            "Sunday": ["Optional light cardio: " + ", ".join(select_exercises("cardio", 1))]
        }
    else:  # experienced
        return {
            "Monday": select_exercises("chest"),
            "Tuesday": select_exercises("back"),
            "Wednesday": select_exercises("legs"),
            "Thursday": select_exercises("shoulders"),
            "Friday": select_exercises("abs"),
            "Saturday": ["Rest / Active recovery (stretching, yoga, foam rolling)"],
            "Sunday": ["Optional full-body cardio: " + ", ".join(select_exercises("cardio", 1))]
        }

# ------------------------
# Endpoint
# ------------------------
@router.post("/plans")
async def generate_plans(request: WorkoutRequest):
    user = await get_user(request.user_id)

    height_m = user["height_in"] * 0.0254
    weight_kg = user["weight_lb"] * 0.453592
    bmi = round(weight_kg / (height_m ** 2), 1)

    return {
        "bmi": bmi,
        "goal": user["goal"],
        "starter_plan": generate_weekly_plan("starter"),
        "experienced_plan": generate_weekly_plan("experienced")
    }