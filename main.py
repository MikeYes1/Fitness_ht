from fastapi import FastAPI, HTTPException
from db import users, workout_plans, meal_plans, chat_history
from db import class_schedule, groceries   # <-- add new collections
from passlib.context import CryptContext
from bson import ObjectId

# -----------------------------
# Password hashing setup
# -----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    if len(password) > 72:  # bcrypt max length
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if len(plain_password) > 72:
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

# -----------------------------
# Mongo Helper
# -----------------------------
def clean_mongo_id(doc: dict) -> dict:
    if not doc:
        return doc
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI with MongoDB!"}

# -----------------------------
# Register & Login
# -----------------------------
@app.post("/register")
def register_user(data: dict):
    if "password" not in data:
        raise HTTPException(status_code=400, detail="Password is required")

    data["password"] = hash_password(data["password"])

    # BMI
    weight = data.get("weight")
    height = data.get("height")
    if weight and height:
        try:
            data["bmi"] = round(weight / ((height / 100) ** 2), 2)
        except Exception:
            data["bmi"] = None
    else:
        data["bmi"] = None

    result = users.insert_one(data)
    new_user = users.find_one({"_id": result.inserted_id}, {"_id": 0, "password": 0})
    return {"status": "User registered successfully", "user": clean_mongo_id(new_user)}

@app.post("/login")
def login_user(credentials: dict):
    user = users.find_one({"username": credentials["username"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(credentials["password"], user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": f"Welcome back {user['username']}!"}

# -----------------------------
# Users
# -----------------------------
@app.get("/get-user/{user_id}")
def get_user(user_id: int):
    user = users.find_one({"id": user_id}, {"_id": 0, "password": 0})
    if not user:
        return {"error": "User not found"}

    workouts = list(workout_plans.find({"userId": user_id}, {"_id": 0}))
    meals = list(meal_plans.find({"userId": user_id}, {"_id": 0}))
    chats = list(chat_history.find({"userId": user_id}, {"_id": 0}))
    classes = list(class_schedule.find({"userId": user_id}, {"_id": 0}))
    grocery_list = list(groceries.find({"userId": user_id}, {"_id": 0}))

    return {
        "user": user,
        "workoutPlans": workouts,
        "mealPlans": meals,
        "chats": chats,
        "classSchedule": classes,
        "groceries": grocery_list,
    }

# -----------------------------
# Workout Plans
# -----------------------------
@app.post("/save-workout-plan")
def save_workout_plan(data: dict):
    result = workout_plans.insert_one(data)
    saved = workout_plans.find_one({"_id": result.inserted_id}, {"_id": 0})
    return {"status": "Workout plan saved", "data": clean_mongo_id(saved)}

@app.get("/get-workout-plan/{user_id}")
def get_workout_plan(user_id: int):
    plans = list(workout_plans.find({"userId": user_id}, {"_id": 0}))
    if plans:
        return {"workoutPlans": plans}
    return {"error": "Workout plans not found"}

# -----------------------------
# Meal Plans
# -----------------------------
@app.post("/save-meal-plan")
def save_meal_plan(data: dict):
    result = meal_plans.insert_one(data)
    saved = meal_plans.find_one({"_id": result.inserted_id}, {"_id": 0})
    return {"status": "Meal plan saved", "data": clean_mongo_id(saved)}

@app.get("/get-meal-plan/{user_id}")
def get_meal_plan(user_id: int):
    plans = list(meal_plans.find({"userId": user_id}, {"_id": 0}))
    if plans:
        return {"mealPlans": plans}
    return {"error": "Meal plans not found"}

# -----------------------------
# Chat History
# -----------------------------
@app.post("/save-chat")
def save_chat(data: dict):
    result = chat_history.insert_one(data)
    saved = chat_history.find_one({"_id": result.inserted_id}, {"_id": 0})
    return {"status": "Chat saved", "data": clean_mongo_id(saved)}

@app.get("/get-chat/{user_id}")
def get_chat(user_id: int):
    chats = list(chat_history.find({"userId": user_id}, {"_id": 0}))
    if chats:
        return {"chats": chats}
    return {"error": "No chat history found"}

# -----------------------------
# Class Schedule
# -----------------------------
@app.post("/save-class-schedule")
def save_class_schedule(data: dict):
    """
    Example:
    {
        "userId": 1,
        "classes": [
            {"day": "Monday", "subject": "Math", "time": "10:00 AM"},
            {"day": "Wednesday", "subject": "Yoga", "time": "6:00 PM"}
        ]
    }
    """
    result = class_schedule.insert_one(data)
    saved = class_schedule.find_one({"_id": result.inserted_id}, {"_id": 0})
    return {"status": "Class schedule saved", "data": clean_mongo_id(saved)}

@app.get("/get-class-schedule/{user_id}")
def get_class_schedule(user_id: int):
    schedule = list(class_schedule.find({"userId": user_id}, {"_id": 0}))
    if schedule:
        return {"classSchedule": schedule}
    return {"error": "No class schedule found"}

# -----------------------------
# Groceries
# -----------------------------
@app.post("/save-groceries")
def save_groceries(data: dict):
    """
    Example:
    {
        "userId": 1,
        "items": ["Chicken", "Eggs", "Broccoli", "Rice"]
    }
    """
    result = groceries.insert_one(data)
    saved = groceries.find_one({"_id": result.inserted_id}, {"_id": 0})
    return {"status": "Groceries saved", "data": clean_mongo_id(saved)}

@app.get("/get-groceries/{user_id}")
def get_groceries(user_id: int):
    grocery_list = list(groceries.find({"userId": user_id}, {"_id": 0}))
    if grocery_list:
        return {"groceries": grocery_list}
    return {"error": "No groceries found"}
