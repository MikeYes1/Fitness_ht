from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import random
from database import db
from bson import ObjectId

router = APIRouter(prefix="/workout", tags=["Workout"])

class WorkoutRequest(BaseModel):
    user_id: str
    level: str  # beginner / intermediate / expert

exercise_pool = {
    "chest": ["Push-ups", "Bench Press", "Incline Bench Press", "Chest Fly", "Cable Crossovers", "Dumbbell Pullover"],
    "back": ["Pull-ups", "Lat Pulldown", "Bent-over Rows", "Seated Cable Row", "T-bar Row", "Superman"],
    "legs": ["Squats", "Lunges", "Leg Press", "Leg Curl", "Calf Raises", "Step-ups"],
    "abs": ["Plank", "Crunches", "Leg Raises", "Bicycle Crunch", "Mountain Climbers", "Russian Twists"],
    "arms": ["Bicep Curls", "Tricep Dips", "Hammer Curls", "Tricep Kickbacks", "Chin-ups", "Close Grip Push-ups"],
    "shoulders": ["Shoulder Press", "Lateral Raises", "Front Raises", "Upright Row", "Arnold Press", "Shrugs"],
    "cardio": ["Jump Rope", "Burpees", "Running", "Cycling", "High Knees", "Jumping Jacks"]
}

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

def generate_plan(level: str) -> Dict[str, List[str]]:
    level = level.lower()
    if level == "beginner":
        return {
            "Monday": select_exercises("chest"),
            "Tuesday": select_exercises("back"),
            "Wednesday": ["Rest / Active recovery (stretching, yoga, light walk)"],
            "Thursday": select_exercises("legs"),
            "Friday": select_exercises("arms"),
            "Saturday": ["Rest"],
            "Sunday": ["Optional light cardio: " + ", ".join(select_exercises("cardio", 1))]
        }
    elif level == "intermediate":
        return {
            "Monday": select_exercises("chest"),
            "Tuesday": select_exercises("back"),
            "Wednesday": select_exercises("legs"),
            "Thursday": select_exercises("shoulders"),
            "Friday": select_exercises("abs"),
            "Saturday": ["Rest / Active recovery (stretching, yoga, foam rolling)"],
            "Sunday": ["Optional full-body cardio: " + ", ".join(select_exercises("cardio", 1))]
        }
    else:  # expert
        return {
            "Monday": select_exercises("chest", 4) + select_exercises("arms", 2),
            "Tuesday": select_exercises("back", 4) + select_exercises("shoulders", 2),
            "Wednesday": select_exercises("legs", 4),
            "Thursday": select_exercises("abs", 3) + select_exercises("cardio", 2),
            "Friday": select_exercises("chest", 3) + select_exercises("arms", 3),
            "Saturday": ["Active recovery: yoga, stretching, light cardio"],
            "Sunday": ["Optional full-body cardio or mobility work"]
        }

@router.post("/plans")
async def generate_plans(request: WorkoutRequest):
    user = await get_user(request.user_id)

    height_m = user["height_in"] * 0.0254
    weight_kg = user["weight_lb"] * 0.453592
    bmi = round(weight_kg / (height_m ** 2), 1)

    plan = generate_plan(request.level)

    # Save to DB
    await db.workoutPlans.update_one(
        {"user_id": user["_id"]},
        {"$set": {
            "user_id": user["_id"],
            "name": user["name"],
            "level": request.level,
            "bmi": bmi,
            "goal": user["goal"],
            "plan": plan
        }},
        upsert=True
    )

    return {
        "user_id": str(user["_id"]),
        "name": user["name"],
        "bmi": bmi,
        "goal": user["goal"],
        "level": request.level,
        "plan": plan
    }