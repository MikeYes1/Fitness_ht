from pymongo import MongoClient
from urllib.parse import quote_plus

# Credentials
username = "thekhetpola_db_user"
password = quote_plus("@Brsbelhasamo98")  # safely encode password

# Connection string
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.s2swqnm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["fitness_ai"]  # database will be created automatically if not exists

# Collections
users = db["users"]
workout_plans = db["workoutPlans"]
meal_plans = db["mealPlans"]
chat_history = db["chatHistory"]

# ✅ Add these new collections
class_schedule = db["classSchedule"]
groceries = db["groceries"]
