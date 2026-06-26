def validateMeals(meals_input):
    valid_meals = ["breakfast", "lunch", "dinner", "snack"]
    meals = [m.strip() for m in meals_input.split(",")]
    invalid = [m for m in meals if m not in valid_meals]
    
    if not invalid:
        return True, meals
    return False, invalid

def validateEmail(email):
    return "@" in email and "." in email

def validateWeight(weight):
    return weight.isdigit() and 50 <= int(weight) <= 500  

def validateAge(age):
    return age.isdigit() and 13 <= int(age) <= 120  

def validateSex(sex):
    return sex in ["male", "female"]

def validateBudget(budget):
    try:
        return float(budget) > 0
    except ValueError:
        return False 

def validateCalories(calories):
    return calories.isdigit() and 1000 <= int(calories) <= 3500

def validateAllergens(allergens_list):
    valid_allergens = ["gluten", "dairy", "peanuts", "soy", "eggs", "shellfish", "fish", "tree nuts", "none"]

    allergens = []  # storing filtered list of separate allergens
    for a in allergens_list.split(","):
      allergens.append(a.strip())

    invalid = []
    for allergen in allergens:
      if allergen not in valid_allergens:
        invalid.append(allergen)

    if invalid:
        return False, invalid
    
    if "none" in allergens:
        return True, []

    return True, allergens




  