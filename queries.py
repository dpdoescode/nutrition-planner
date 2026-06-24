from database import get_connection

# insert new user into the database
def add_user(username, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, email)
        VALUES (? , ?)
        """, (username, email))

    conn.commit()
    conn.close()

# fetch a single user by username
def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE username = ?
        """, (username,))

    user = cursor.fetchone()
    conn.close()
    return user

# insert nutritional goals for a user
def add_user_goals(user_id, calorie_goal, protein_goal_g, budget_weekly, calcium_mg, iron_mg, potassium_mg, vitamin_c_mg):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_goals (user_id, calorie_goal, protein_goal_g, budget_weekly, calcium_mg, iron_mg, potassium_mg, vitamin_c_mg)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, calorie_goal, protein_goal_g, budget_weekly, calcium_mg, iron_mg, potassium_mg, vitamin_c_mg))

    conn.commit()
    conn.close()

# fetch goals for a given user
def get_user_goals(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM user_goals WHERE user_id = ?
        """, (user_id,))
    
    goals = cursor.fetchone()
    conn.close()
    return goals

# insert allergens for a user
def add_user_allergen(user_id, allergen):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_allergens (user_id, allergen)
        VALUES (? , ?)
        """, (user_id, allergen))

    conn.commit()
    conn.close()

# fetch all allergens for a given user
def get_user_allergens(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM user_allergens WHERE user_id = ?
        """, (user_id,))
    
    allergens = cursor.fetchall()  # fetch all because user can have multiple allergens
    conn.close()
    return allergens

# insert meal preferences for a user
def add_user_meal_preference(user_id, meal_name, meal_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_meal_preferences (user_id, meal_name, meal_type)
        VALUES (?, ?, ?)
        """, (user_id, meal_name, meal_type))

    conn.commit()
    conn.close()

# fetch all meal preferences for a given user
def get_user_meal_preferences(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM user_meal_preferences WHERE user_id = ?
    """, (user_id,))
    
    meals = cursor.fetchall()
    conn.close()
    return meals

# insert meal plan for a user
def add_meal_plans(user_id, plan_date, api_response, total_calories, total_protein_g, estimated_cost):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO meal_plans(user_id, plan_date, api_response, total_calories, total_protein_g, estimated_cost)
        VALUES (?, ?, ?, ?, ?, ?) 
        """, (user_id, plan_date, api_response, total_calories, total_protein_g, estimated_cost))

    conn.commit()
    conn.close()

#fetch most recent meal plan for a given user
def get_meal_plans(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM meal_plans WHERE user_id = ?
        """, (user_id,))
    
    plan = cursor.fetchone()
    conn.close()
    return plan

if __name__ == "__main__":
    add_user("mali2", "mali2@fsu.edu")
    user = get_user("mali2")
    print(user["username"], user["email"])

    add_user_goals(1, 2000, 150, 50.00, 1000, 18, 3400, 90)
    goals = get_user_goals(1)
    print(goals["calorie_goal"], goals["protein_goal_g"], goals["budget_weekly"])
    print(goals["calcium_mg"], goals["iron_mg"], goals["potassium_mg"], goals["vitamin_c_mg"])

    add_user_allergen(1, "gluten")
    add_user_allergen(1, "dairy")
    allergens = get_user_allergens(1)
    for a in allergens:
        print(a["allergen"])
    
    add_user_meal_preference(1, "eggs", "breakfast")
    add_user_meal_preference(1, "grilled chicken", "dinner")
    meals = get_user_meal_preferences(1)
    for m in meals:
        print(m["meal_name"], m["meal_type"])
    
    add_meal_plans(1, "2026-06-24", "{}", 2000, 150, 50.00)
    plan = get_meal_plans(1)
    print(plan["plan_date"], plan["total_calories"], plan["estimated_cost"])

    