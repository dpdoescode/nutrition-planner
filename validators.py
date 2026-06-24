def validateMeals(meals_input):
    valid_meals = ["breakfast", "lunch", "dinner", "snack"]
    meals = [m.strip() for m in meals_input.split(",")]
    invalid = [m for m in meals if m not in valid_meals]
    
    if not invalid:
        return True, meals
    return False, invalid

def validateDays(days):
  return days.isdigit() and 1 <= int(days) <= 7

def validateEmail(email):
    return "@" in email and "." in email

def validateWeight(weight):
    return weight.isdigit() and 50 <= int(weight) <= 500  

def validateWeight(age):
    return age.isdigit() and 13 <= int(age) <= 120  

def validateWeight(sex):
    return sex.islower() in ["male", "female"]

def validateBudget(budget):
    try:
        return float(budget) > 0
    except ValueError:
        return False 




  