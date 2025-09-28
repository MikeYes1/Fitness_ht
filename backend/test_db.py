# test_db.py
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        print("MONGODB_URI not set")
        return
    try:
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        db = client.get_default_database()
        if db is None:
            db = client.fitness_ai  # fallback DB name
        cols = await db.list_collection_names()
        print("Connected! Collections:", cols)
    except Exception as e:
        print("Connection failed:", repr(e))

asyncio.run(test())