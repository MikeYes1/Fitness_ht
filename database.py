# database.py
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("Set the MONGODB_URI environment variable")

client = AsyncIOMotorClient(MONGODB_URI)
db = client.fitness_ai  # your database name