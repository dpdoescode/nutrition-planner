from queries import get_user, get_user_goals, add_user, add_user_goals, add_meal_plans, get_user_allergens, add_user_allergen
from validators import validateMeals, validateEmail, validateWeight, validateAge, validateSex, validateBudget, validateCalories, validateAllergens
from datetime import date
import requests
import random
import time
import json
import os

mealplan_api = os.getenv('MEALPLAN_API')
mealplan_appid = 'b4a47ae5'
userid = 'cli_user_1'
BASE_URL = "https://api.edamam.com/api/recipes/v2" 

spoonacular_api = os.getenv('SPOONACULAR_API')
spoonacular_url = "https://api.spoonacular.com/recipes" 

# maps each meal to its API params
MEAL_CONFIG = {
    "breakfast": {"mealType": "breakfast", "dishType": ["egg", "bread", "cereals", "pancake", "pastry"]},
    "lunch":     {"mealType": "lunch/dinner", "dishType": ["salad", "soup", "sandwiches", "starter", "side dish"]},
    "dinner":    {"mealType": "lunch/dinner", "dishType": ["main course", "pasta", "seafood", "pizza", "casserole", "pies and tarts"]},
    "snack":     {"mealType": "snack", "dishType": ["drinks", "biscuits and cookies", "sweets", "ice cream and custard"]}
}

def getUsernameInput():
  while True:
    username = input("Enter username: ").strip()
    if username:
      return username
    print("Must have a username")

def getEmailInput():
  while True:
    email = input("Enter email: ").strip()
    if validateEmail(email):
      return email
    print("Enter valid email address")

def getWeightInput():
  while True:
    weight = input("Enter weight (lbs): ").strip()
    if validateWeight(weight):
      return int(weight)
    print("Enter valid weight between 50 and 500 lbs")

def getAgeInput():
  while True:
    age = input("Enter age: ").strip()
    if validateAge(age):
      return int(age)
    print("Enter valid age between 13 and 120")

def getSexInput():
  while True:
    sex = input("Enter sex (male/female): ").strip().lower()
    if validateSex(sex):
      return sex
    print("Enter male or female") 

def getBudgetInput():
  while True:
    budget = input("Weekly budget ($): ").strip()
    if validateBudget(budget):
      return float(budget)
    print("Enter a valid number above 0") 

def getCaloriesInput():
  while True:
    calories = input("Daily calorie goal: ").strip()
    if validateCalories(calories):
      return int(calories)
    print("Enter a number between 1000 and 3500") 

def calculateNutrientGoals(weight, age, sex):
  protein = round(weight * 0.36)
  if age <= 18:
    calcium = 1300
  elif age <= 50:
    calcium = 1000 
  else:
    calcium = 1200
  
  if sex == "male":
    iron = 8
  elif age <= 50:
    iron = 18 
  else:
    iron = 8

  potassium = 3400 if sex == "male" else 2600
  vitamin_c = 90 if sex == "male" else 75
  return {
    "protein" : protein,
    "calcium" : calcium,
    "iron" : iron,
    "potassium" : potassium,
    "vitamin_c" : vitamin_c
  }

def getAllergensInput():
  while True:
    allergens_list = input("Any allergens? (gluten, dairy, peanuts, soy, eggs, shellfish, fish, tree nuts, or none): ").strip().lower()
    
    valid, result = validateAllergens(allergens_list)

    if valid:
      return result
    
    print(f"Invalid allergens: {', '.join(result)}")
    
def loginOrRegister():
  username = getUsernameInput()
  user = get_user(username)
  if user:
    print(f"Welcome back!")

    # allergen info 
    allergens = get_user_allergens(user[0])
    if allergens:
      print(f"Here are your logged allergens: {', '.join(allergens)}")
    else:
      print("You have no logged allergens.")
      
    # all goals
    goals = get_user_goals(user[0])
    if goals:
      calorie_goal = goals[2] if goals else 2000  # hardcode calorie goal if no goals exist for user
      protein_goal = goals[3] if goals else 120  # hardcode protein goal if no goals exist for user
      budget = goals[4] if goals else 100.0
      calcium_goal = goals[5]
      iron_goal = goals[6]
      potassium_goal = goals[7]
      vitamin_c_goal = goals[8]
      print(f"-- Here are your daily goals --")
      print(f"  Calories:   {calorie_goal}")
      print(f"  Protein:    {protein_goal}g")
      print(f"  Budget:     ${budget}/week")
      print(f"  Calcium:    {calcium_goal}mg")
      print(f"  Iron:       {iron_goal}mg")
      print(f"  Potassium:  {potassium_goal}mg")
      print(f"  Vitamin C:  {vitamin_c_goal}mg\n")
    else:
      print("You have no logged goals.")
      
    return user[0], allergens, calorie_goal, budget, protein_goal, calcium_goal, iron_goal, potassium_goal, vitamin_c_goal
  else:
    print("Username not found, let's setup your profile!")
    # else get user input for new user
    email = getEmailInput()
    weight = getWeightInput()
    age = getAgeInput()
    sex = getSexInput()
    budget = getBudgetInput()
    allergens = getAllergensInput()  # list of valid allergens
    calorie_goal = getCaloriesInput()
    nutrients = calculateNutrientGoals(weight, age, sex)
    protein_goal = nutrients["protein"]
    calcium_goal = nutrients["calcium"]
    iron_goal = nutrients["iron"]
    potassium_goal = nutrients["potassium"]
    vitamin_c_goal = nutrients["vitamin_c"]

    print(f"\nCalculated daily goals:")
    print(f"  Protein:    {protein_goal}g")
    print(f"  Calcium:    {nutrients['calcium']}mg")
    print(f"  Iron:       {nutrients['iron']}mg")
    print(f"  Potassium:  {nutrients['potassium']}mg")
    print(f"  Vitamin C:  {nutrients['vitamin_c']}mg\n")

    add_user(username, email)
    user = get_user(username)
    add_user_goals(user[0], calorie_goal, protein_goal, budget, calcium_goal, iron_goal, potassium_goal, vitamin_c_goal)
    for allergen in allergens:
      add_user_allergen(user[0], allergen)

    return user[0], allergens, calorie_goal, budget, protein_goal, calcium_goal, iron_goal, potassium_goal, vitamin_c_goal
    

ALLERGENS_MAP = {  # maps user-friendly allergen names to API parameters
  "gluten" : "GLUTEN_FREE",
  "dairy" : "DAIRY_FREE",
  "peanuts" : "PEANUT_FREE",
  "soy" : "SOY_FREE",
  "eggs" : "EGG_FREE",
  "shellfish" : "SHELLFISH_FREE",
  "fish" : "FISH_FREE",
  "tree nuts" : "TREE_NUT_FREE",
}
recipe_cache = {}  # reusing recipes instead of calling the API again for speed
used_recipes = {}  # track used recipe names per meal
def getRecipeForMeal(meal, allergens, calorie_goal):
  if meal not in used_recipes: 
    used_recipes[meal] = set()

  if meal in recipe_cache:  # check if meal already has a recipe cached
    available = [r for r in recipe_cache[meal] if r["name"] not in used_recipes[meal]]
    if available: 
      recipe = random.choice(available)  # return a random recipe from the cached list
      used_recipes[meal].add(recipe["name"])  # add to seen recipes to avoid duplicates.
      return recipe

  config = MEAL_CONFIG[meal]  # looks up whichever meal was passed in
  dish = random.choice(config['dishType'])  # selects random dish because Recipe Search API only accepts one dishType at a time -- we want to avoid giving the same dishType
  
  params = {
      "type" : "public",
      "app_id": mealplan_appid,
      "app_key": mealplan_api,
      "mealType": config["mealType"],
      "dishType": dish,
      "from" : 0,
      "to": 100  # request up to 100 recipes
  }
  time.sleep(4)  # add a delay to avoid hitting the API too quickly and getting rate limited
  response = requests.get(BASE_URL, params=params)
  # print(response.status_code) to verify response status code
  #  handle rate limit errors...
  if response.status_code == 429:
      print("  Rate limited, waiting 8 seconds...")
      time.sleep(8)
      response = requests.get(BASE_URL, params=params)
        
  if response.status_code != 200:
    return None

  hits = response.json().get("hits", [])
  # print(f"Hits: {len(hits)}") verifying fetch hit
  if not hits:
    return None

  recipes = []
  for hit in hits[:100]:
    recipe = hit["recipe"] 
    nutrients = recipe["totalNutrients"]
    calories = round(nutrients["ENERC_KCAL"]["quantity"])
    recipe_health = recipe.get("healthLabels", [])

    # skip if doesn't meet allergen requirements
    skip = False
    for allergen in allergens:
        label = ALLERGENS_MAP.get(allergen)
        if label and label not in recipe_health:
            skip = True
            break
    if skip:
        continue

    # skip if outside calorie range
    cal_per_meal = round(calorie_goal / len(meals))
    cal_min = round(cal_per_meal * 0.3)
    cal_max = round(cal_per_meal * 1.5)
    if not (cal_min <= calories <= cal_max):
        continue

    recipes.append({
      "name": recipe["label"],
      "calories": calories,
      "protein": round(recipe["totalNutrients"]["PROCNT"]["quantity"]),
      "calcium": round(nutrients["CA"]["quantity"]),
      "iron": round(nutrients["FE"]["quantity"]),
      "potassium": round(nutrients["K"]["quantity"]),
      "vitamin_c": round(nutrients["VITC"]["quantity"]),
      "url": recipe["url"],
      "ingredients": recipe.get("ingredientLines", [])
    })

  if not recipes:
    return None
  
  recipe_cache[meal] = recipes  # cache the recipes for future use
  recipe = random.choice(recipes)
  used_recipes[meal].add(recipe["name"])  # add to seen recipes to avoid duplicates.
  return recipe  # return a random recipe from the list

def getRecipePrice(ingredients):
  ingredient_str = ", ".join(ingredients) # convert list to a string: 2 cups flour, 1 tbsp butter, 3 eggs

  search = requests.get(f"{spoonacular_url}/findByIngredients", params={
    "ingredients": ingredient_str,  # pass ingredients as search query
    "apiKey": spoonacular_api,
    "number": 1
  })

  results = search.json() # parse response as JSON

  if not isinstance(results, list) or not results:
    print("Spoonacular error:", results)
    return 0.0
  
  recipe_id = results[0]["id"] # grab spoonacular recipe id from first result

  # use that id to get the price breakdown for that recipe
  price = requests.get(f"https://api.spoonacular.com/recipes/{recipe_id}/priceBreakdownWidget.json", params={
    "apiKey": spoonacular_api
  })
  if price.status_code != 200:  # safety in case of API error
    return 0.0

  data = price.json()
  return round(data.get("totalCost", 0) / 100, 2)
  
def warmCache(meals, allergens, calorie_goal):
  print("Loading recipes...\n")
  for meal in meals:
    if meal not in recipe_cache:
      print(f"  Loading {meal} recipes...")
      getRecipeForMeal(meal, allergens, calorie_goal)
      time.sleep(15)

def fetchMealPlan(meals, allergens, calorie_goal):
  warmCache(meals, allergens, calorie_goal)

  meal_plan = {}
  for day in range(1, 3):  # hardcoded to 7 days (8 - 1)
    meal_plan[day] = {}
    for meal in meals:
      print(f"  Building Day {day} {meal.capitalize()}...")
      meal_plan[day][meal] = getRecipeForMeal(meal, allergens, calorie_goal)

  return meal_plan

def storeMealPlan(user_id, meal_plan, meals):
  total_calories = 0
  total_protein = 0
  total_calcium = 0
  total_iron = 0
  total_potassium = 0
  total_vitamin_c = 0

  for day in range(1, 3):  # hardcoded to 7 days (8 - 1)
    for meal in meals:
      recipe = meal_plan[day][meal]
      if recipe:
        total_calories += recipe["calories"]
        total_protein += recipe["protein"]
        total_calcium += recipe["calcium"]
        total_iron += recipe["iron"]
        total_potassium += recipe["potassium"]
        total_vitamin_c += recipe["vitamin_c"]

  avg_calories = round(total_calories/2)  # divided by hardcoded 7 days
  avg_protein = round(total_protein/2)  # divided by hardcoded 7 days
  add_meal_plans(
    user_id,
    str(date.today()),
    json.dumps(meal_plan),
    avg_calories, 
    avg_protein,
    0.00
  )
  print("Meal plan saved!")


def displayMealPlan(meal_plan, meals, budget, calorie_goal, protein_goal, calcium_goal, iron_goal, potassium_goal, vitamin_c_goal):
  print("\n=== Your Meal Plan ===\n")
  total_cost = 0.0 
  for day in range(1, 3):  # hardcoded to 7 days (8 - 1)
    print(f"--- Day {day} ---")
    day_calories = 0
    for meal in meals:
      recipe = meal_plan[day][meal]
      if not recipe:
        print(f"  {meal.capitalize()}: No recipe found")
      else:
        price = getRecipePrice(recipe["ingredients"])
        total_cost += price
        day_calories += recipe["calories"]
        print(f"  {meal.capitalize()}: {recipe['name']}")
        print(f"    Calories: {recipe['calories']} | Protein: {recipe['protein']}g | Calcium: {recipe['calcium']}mg | Iron: {recipe['iron']}mg | Potassium: {recipe['potassium']}mg | Vitamin C: {recipe['vitamin_c']}mg")
        print(f"    Est. Cost: ${price}")
        print(f"    URL: {recipe['url']}")
    print(f"  Day Total: {day_calories} cal (goal: {calorie_goal})")
    print()
  print(f"Estimated Total Weekly Cost: ${round(total_cost, 2)}")
  if total_cost > budget:
    print(f"⚠️  Over budget by ${round(total_cost - budget, 2)} (Budget: ${budget})")
  else:
    print(f"✓ Within budget! ${round(budget - total_cost, 2)} remaining (Budget: ${budget})")



user_id, allergens, calorie_goal, budget, protein_goal, calcium_goal, iron_goal, potassium_goal, vitamin_c_goal = loginOrRegister()

# get which meals the user wants to eat per day
while True:
    meals_input = input("Which meals? (breakfast, lunch, dinner, snack): ").strip().lower()
    is_valid, result = validateMeals(meals_input)
    
    if is_valid:
        meals = result  # meals is a list of valid meals
        break
    
    print(f"Invalid meals: {', '.join(result)}")
    print(f"Valid options: breakfast, lunch, dinner, snack")

print("\nFetching your meal plan...\n")
meal_plan = fetchMealPlan(meals, allergens, calorie_goal)
storeMealPlan(user_id, meal_plan, meals)
displayMealPlan(meal_plan, meals, budget, calorie_goal, protein_goal, calcium_goal, iron_goal, potassium_goal, vitamin_c_goal)