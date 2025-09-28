#!/bin/bash

# Backend in a new terminal window
osascript -e 'tell application "Terminal" to do script "cd ~/projects/Fitness_ht/backend; source venv/bin/activate; export MONGODB_URI=\"mongodb+srv://Akil_Talakola:hellosiri123@cluster0.s2swqnm.mongodb.net/fitness_ai?retryWrites=true&w=majority\"; export SPOONACULAR_API_KEY=\"6db529071dab4a1c8674bf7660f955fd\"; uvicorn main:app --reload --port 8001"'

# Frontend in a new terminal window
osascript -e 'tell application "Terminal" to do script "cd ~/projects/frontend; npm install; npm run dev"'
