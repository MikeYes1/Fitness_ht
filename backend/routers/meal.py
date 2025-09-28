from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests, os
from database import db
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/meal", tags=["Meal"])

class MealRequest(BaseModel):
    user_id: str

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
if not SPOONACULAR_API_KEY:
    raise ValueError("Set the SPOONACULAR_API_KEY environment variable")

async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def calculate_calories(weight_lb, height_in, age, gender, goal):
    weight_kg = weight_lb * 0.453592
    height_cm = height_in * 2.54
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age
    bmr += 5 if gender.lower() == "male" else -161
    tdee = bmr * 1.55
    if goal.lower() == "lose weight":
        tdee -= 500
    elif goal.lower() == "gain muscle":
        tdee += 300
    macros = {
        "protein_g": round((0.3 * tdee) / 4),
        "carbs_g": round((0.4 * tdee) / 4),
        "fat_g": round((0.3 * tdee) / 9),
        "sugar_g": round((0.1 * tdee) / 4)
    }
    return round(tdee), macros

def map_diet(pref: str):
    pref = pref.lower()
    if "vegetarian" in pref: return "vegetarian"
    if "vegan" in pref: return "vegan"
    if "keto" in pref: return "ketogenic"
    if "paleo" in pref: return "paleo"
    return None

@router.post("/generate")
async def generate_meal_plan(request: MealRequest):
    user = await get_user(request.user_id)

    daily_calories, macros = calculate_calories(
        user["weight_lb"], user["height_in"], user["age"], user["gender"], user["goal"]
    )
    diet_filter = map_diet(user["dietary_preferences"])

    params = {
        "number": 21,
        "addRecipeInformation": True,
        "apiKey": SPOONACULAR_API_KEY
    }
    if diet_filter: params["diet"] = diet_filter

    response = requests.get(
        "https://api.spoonacular.com/recipes/complexSearch",
        params=params
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching meal data")

    all_recipes = response.json().get("results", [])

    meal_plan = {}
    for day in range(7):
        day_key = f"Day {day + 1}"
        meals = {"breakfast": [], "lunch": [], "dinner": []}
        for i in range(3):  # 3 meals per day
            idx = day * 3 + i
            if idx < len(all_recipes):
                recipe = all_recipes[idx]
                meal_type = ["breakfast", "lunch", "dinner"][i]
                meals[meal_type].append({
                    "title": recipe.get("title"),
                    "readyInMinutes": recipe.get("readyInMinutes"),
                    "servings": recipe.get("servings"),
                    "sourceUrl": recipe.get("sourceUrl")
                })
        meal_plan[day_key] = meals