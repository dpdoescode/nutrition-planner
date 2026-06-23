import requests
import json
import os

mealplan_api = os.getenv('MEALPLAN_API')
mealplan_appid = 'c790d706'
userid = 'cli_user_1'

url = 'https://api.edamam.com/api/meal-planner/v1/{mealplan_appid}/select'
# response = requests.post(url, )

