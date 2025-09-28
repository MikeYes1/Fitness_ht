from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, workout, meal, quotes, users

app = FastAPI()

# === CORS configuration ===
origins = [
    "http://localhost:3000",  # your frontend URL
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allow these origins
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],         # allow all headers
)

# === Routers ===
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(workout.router)
app.include_router(meal.router)
app.include_router(quotes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Fitness AI backend"}