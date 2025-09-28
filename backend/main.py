from fastapi import FastAPI
from routers import chat, workout, meal, quotes, users

app = FastAPI()

app.include_router(users.router)
app.include_router(chat.router)
app.include_router(workout.router)
app.include_router(meal.router)
app.include_router(quotes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Fitness AI backend"}