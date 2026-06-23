def mealValidation(s):
  valid_meals = ["breakfast", "lunch", "dinner", "snack"]

  while True:
    meals_input = input("Which meals? (breakfast, lunch, dinner, snack): ").strip().lower()
    meals = [s.strip() for s in meals_input.split(",")]
    
    invalid = [s for s in meals if s not in valid_meals]
    
    if not invalid:
      break
    
    print(f"Invalid meals: {', '.join(invalid)}")
    print(f"Valid options: {', '.join(valid_meals)}")
  