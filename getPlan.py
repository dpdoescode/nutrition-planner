import requests
import json
import os

mealplan_api = os.getenv('MEALPLAN_API')
mealplan_appid = 'c790d706'
userid = 'cli_user_1'

url = 'https://api.edamam.com/api/meal-planner/v1/{mealplan_appid}/select'
# response = requests.post(url, )
response = requests.get(url)

meals = ['breakfast', 'lunch', 'dinner', 'snack']

meal = input("Which meals do you eat per day?(breakfast, lunch, dinner, snack): ")



#print(response.json())