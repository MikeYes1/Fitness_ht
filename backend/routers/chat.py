from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
from database import db
from bson import ObjectId
import requests, re

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    user_id: str
    message: str

# Load Flan-T5 model
model_name = "google/flan-t5-large"
device = 0 if torch.cuda.is_available() else -1

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

chat_pipeline = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device=device,
    max_new_tokens=200,
    do_sample=True,
    top_p=0.9,
    temperature=0.8
)

exercise_keywords = [
    "push-up", "bench press", "squat", "lunge", "curl", "pull-up", "deadlift",
    "plank", "bicep curl", "tricep dip", "shoulder press", "leg press"
]

async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_exercise_info(exercise_name: str) -> str:
    url = f"https://wger.de/api/v2/exercise/?language=2&search={exercise_name}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return "No detailed instructions available."
        data = response.json()
        results = data.get("results")
        if not results:
            return "No detailed instructions available."
        desc = results[0].get("description", "")
        desc = re.sub(r"<.*?>", "", desc)
        return desc.strip() or "No detailed instructions available."
    except Exception:
        return "No detailed instructions available."

@router.post("/send")
async def send_message(request: ChatRequest):
    user = await get_user(request.user_id)

    exercise_in_question = next(
        (word for word in exercise_keywords if word.lower() in request.message.lower()), None
    )

    if exercise_in_question:
        instructions = get_exercise_info(exercise_in_question)
        prompt = f"""
You are a professional fitness coach.
Provide beginner-friendly, step-by-step instructions for the exercise '{exercise_in_question}'.
User profile: {user['age']} years old, {user['gender']}, {user['weight_lb']} lbs, {user['height_in']} inches, Goal: {user['goal']}.
Exercise details from API: {instructions}
Include 2-3 actionable steps on form, safety, and beginner tips.
Stop after giving the steps; do not repeat yourself.
"""
    else:
        prompt = f"""
You are a professional fitness and nutrition coach.
Answer the user query in a beginner-friendly way tailored to the user:
Age: {user['age']}, Gender: {user['gender']}, Weight: {user['weight_lb']} lbs, Height: {user['height_in']} inches, Goal: {user['goal']}.
Provide 3-4 actionable tips.
Include advice for hydration, stress management, mindful eating, snacks, motivation, and exercise form if relevant.
Stop after giving the steps; do not repeat yourself.

User question: {request.message}
Assistant:
"""

    result = chat_pipeline(prompt)[0]["generated_text"]
    for stop_word in ["User question:", "Assistant:"]:
        if stop_word in result:
            result = result.split(stop_word)[0].strip()

    return {"reply": result}