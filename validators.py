def validateMeals(meals_input):
    valid_meals = ["breakfast", "lunch", "dinner", "snack"]
    meals = [m.strip() for m in meals_input.split(",")]
    invalid = [m for m in meals if m not in valid_meals]
    
    if not invalid:
        return True, meals
    return False, invalid

def validateDays(days):
  return days.isdigit() and 1 <= int(days) <= 7



  