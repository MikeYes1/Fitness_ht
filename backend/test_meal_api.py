import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")
if not API_KEY:
    raise ValueError("SPOONACULAR_API_KEY not set")

url = "https://api.spoonacular.com/recipes/complexSearch"
params = {
    "number": 5,
    "addRecipeInformation": True,
    "apiKey": API_KEY
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Success! Recipes fetched:")
    for recipe in data.get("results", []):
        print("-", recipe.get("title"), recipe.get("sourceUrl"))
else:
    print("Failed:", response.status_code, response.text)