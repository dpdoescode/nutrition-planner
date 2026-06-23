from validators import validateDays, validateMeals
import requests
import json
import os

mealplan_api = os.getenv('MEALPLAN_API')
mealplan_appid = 'c790d706'
userid = 'cli_user_1'

url = 'https://api.edamam.com/api/meal-planner/v1/{mealplan_appid}/select'
response = requests.get(url)

# get which meals the user wants to eat per day
while True:
    meals_input = input("Which meals? (breakfast, lunch, dinner, snack): ").strip().lower()
    is_valid, result = validateMeals(meals_input)
    
    if is_valid:
        meals = result
        break
    
    print(f"Invalid meals: {', '.join(result)}")
    print(f"Valid options: breakfast, lunch, dinner, snack")

# get number of day the user wants to plan
while True: 
  days = input("How many days do you want to plan meals for? (1-7): ").strip()
  if validateDays(days):
    days = int(days)# cast to int if valid
    break # break loop if valid
  print("Enter a number between 1 and 7")

#print(response.json())