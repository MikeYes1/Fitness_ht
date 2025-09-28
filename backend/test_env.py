# test_env.py
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get your Spoonacular API key
api_key = os.getenv("SPOONACULAR_API_KEY")

# Check if it loaded correctly
if api_key:
    print("SPOONACULAR_API_KEY loaded successfully:", api_key)
else:
    print("SPOONACULAR_API_KEY not found. Check your .env file!")