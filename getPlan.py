from validators import validateDays, validateMeals
import requests
import random
import time
import json
import os

mealplan_api = os.getenv('MEALPLAN_API')
mealplan_appid = 'b4a47ae5'
userid = 'cli_user_1'
BASE_URL = "https://api.edamam.com/api/recipes/v2" 

# get which meals the user wants to eat per day
while True:
    meals_input = input("Which meals? (breakfast, lunch, dinner, snack): ").strip().lower()
    is_valid, result = validateMeals(meals_input)
    
    if is_valid:
        meals = result  # meals is a list of valid meals
        break
    
    print(f"Invalid meals: {', '.join(result)}")
    print(f"Valid options: breakfast, lunch, dinner, snack")

#  get number of day the user wants to plan
while True: 
  days = input("How many days do you want to plan meals for? (1-7): ").strip()
  if validateDays(days):
    days = int(days)
    break
  print("Enter a number between 1 and 7")

# maps each meal to its API params
MEAL_CONFIG = {
    "breakfast": {"mealType": "breakfast", "dishType": ["egg", "bread", "cereals", "pancake"]},
    "lunch":     {"mealType": "lunch/dinner", "dishType": ["salad", "soup", "sandwiches"]},
    "dinner":    {"mealType": "lunch/dinner", "dishType": ["main course", "pasta", "seafood"]},
    "snack":     {"mealType": "snack", "dishType": ["drinks", "biscuits and cookies"]}
}

def getRecipesForMeal(meal, count): 
  config = MEAL_CONFIG[meal]  # looks up whichever meal was passed in
  dish = random.choice(config['dishType'])  # selects random dish because Recipe Search API only accepts one dishType at a time -- we want to avoid giving the same dishType

  params = {
      "type" : "public",
      "app_id": mealplan_appid,
      "app_key": mealplan_api,
      "mealType": config["mealType"],
      "dishType": dish
  }

  time.sleep(3)  # add a delay to avoid hitting the API too quickly and getting rate limited
  response = requests.get(BASE_URL, params=params)
  #  handle rate limit errors...
  if response.status_code == 429:
      print("  Rate limited, waiting 15 seconds...")
      time.sleep(15)
      response = requests.get(BASE_URL, params=params)
        
  if response.status_code != 200:
    return []

  hits = response.json().get("hits", [])
  recipes = []
  for hit in hits[:count]:
      recipe = hit["recipe"]
      recipes.append({
          "name": recipe["label"],
          "calories": round(recipe["totalNutrients"]["ENERC_KCAL"]["quantity"]),
          "protein": round(recipe["totalNutrients"]["PROCNT"]["quantity"]),
          "url": recipe["url"]
      })
  return recipes

print("\n=== Your Meal Plan ===\n")

# fetch recipes per meal type once (not once per day)
meal_recipes = {}
for meal in meals:
    print(f"Fetching {meal} recipes...")
    meal_recipes[meal] = getRecipesForMeal(meal, days)
    time.sleep(5)

# display plan using fetched recipes
for day in range(1, days + 1):
    print(f"--- Day {day} ---")
    for meal in meals:
        recipes = meal_recipes[meal]
        if recipes is None or day > len(recipes):
            print(f"  {meal.capitalize()}: No recipe found")
        else:
            recipe = recipes[day - 1]
            print(f"  {meal.capitalize()}: {recipe['name']}")
            print(f"  Calories: {recipe['calories']} | Protein: {recipe['protein']}g")
            print(f"  URL: {recipe['url']}")
    print()