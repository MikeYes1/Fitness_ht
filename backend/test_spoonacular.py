# test_spoonacular.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")
url = "https://api.spoonacular.com/recipes/complexSearch"
params = {
    "apiKey": API_KEY,
    "number": 5,  # fetch 5 recipes as a test
    "addRecipeInformation": True
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Recipes fetched successfully!")
    for i, recipe in enumerate(data.get("results", []), 1):
        print(f"{i}. {recipe['title']} - {recipe['sourceUrl']}")
else:
    print(f"Failed: {response.status_code} {response.text}")