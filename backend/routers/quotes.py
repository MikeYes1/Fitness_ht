# routers/quotes.py
from fastapi import APIRouter
import random

router = APIRouter(prefix="/quotes", tags=["Quotes"])

quotes_list = [
    "The only bad workout is the one that didn’t happen.",
    "Push yourself because no one else is going to do it for you.",
    "Fitness is not about being better than someone else. It's about being better than you used to be.",
    "Motivation is what gets you started. Habit is what keeps you going.",
    "Sweat is fat crying.",
    "Strive for progress, not perfection.",
    "The pain you feel today will be the strength you feel tomorrow.",
    "Your body can stand almost anything. It’s your mind that you have to convince."
]

@router.get("/")
async def get_random_quote():
    return {"quote": random.choice(quotes_list)}