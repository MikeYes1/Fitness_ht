# routers/quotes.py
from fastapi import APIRouter
import random
import datetime

router = APIRouter(prefix="/quotes", tags=["Quotes"])

# Quote pool
QUOTES = {
    "general": [
        "The only bad workout is the one that didn't happen.",
        "Strive for progress, not perfection.",
        "Consistency is more important than intensity.",
        "Your body can stand almost anything. It’s your mind you have to convince.",
        "Don't wish for it, work for it."
    ],
    "fitness": [
        "Push yourself because no one else is going to do it for you.",
        "Sweat is just fat crying.",
        "The pain you feel today will be the strength you feel tomorrow."
    ],
    "nutrition": [
        "Eat to fuel your body, not to feed your emotions.",
        "You are what you eat, so don't be fast, cheap, easy, or fake.",
        "Nutrition is not about restriction, it's about balance."
    ],
    "motivation": [
        "Success starts with self-discipline.",
        "Small steps every day lead to big results.",
        "The difference between wanting and achieving is action."
    ]
}

@router.get("/random")
def get_random_quote(category: str = "general"):
    """
    Return a random motivational quote.
    Optional query parameter: category (general, fitness, nutrition, motivation).
    """
    category = category.lower()
    quotes_list = QUOTES.get(category, QUOTES["general"])
    return {"quote": random.choice(quotes_list)}

@router.get("/daily")
def get_daily_quote(category: str = "general"):
    """
    Return a 'Quote of the Day'.
    The same quote will be shown to everyone for the day.
    """
    category = category.lower()
    quotes_list = QUOTES.get(category, QUOTES["general"])

    # Use today's date as a seed so the quote is consistent each day
    today = datetime.date.today().toordinal()
    random.seed(today)  # same seed = same quote for the day
    quote = random.choice(quotes_list)

    return {
        "date": str(datetime.date.today()),
        "quote": quote
    }