from database import get_connection

def add_user(username, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, email)
        VALUES (? , ?)
        """, (username, email))

    conn.commit()
    conn.close()

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE username = ?
        """, (username,))

    user = cursor.fetchone()
    conn.close()
    return user

def add_user_goals(user_id, calorie_goal, protein_goal_g, budget_weekly):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_goals (user_id, calorie_goal, protein_goal_g, budget_weekly)
        VALUES (?, ?, ?, ?)
        """, (user_id, calorie_goal, protein_goal_g, budget_weekly))

    conn.commit()
    conn.close()

def get_user_goals(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM user_goals WHERE user_id = ?
        """, (user_id,))
    
    goals = cursor.fetchone()
    conn.close()
    return goals

def add_user_allergen(user_id, allergen):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_allergens (user_id, allergen)
        VALUES (? , ?)
        """, (user_id, allergen))

    conn.commit()
    conn.close()

def get_user_allergens(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM user_allergens WHERE user_id = ?
        """, (user_id,))
    
    allergens = cursor.fetchall()  # fetch all because user can have multiple allergens
    conn.close()
    return allergens

def add_user_meal_preference(user_id, meal_name, meal_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_meal_preferences (user_id, meal_name, meal_type)
        VALUES (?, ?, ?)
        """, (user_id, meal_name, meal_type))

    conn.commit()
    conn.close()

def get_user_meal_preferences(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM user_meal_preferences WHERE user_id = ?
    """, (user_id,))
    
    meals = cursor.fetchall()
    conn.close()
    return meals


if __name__ == "__main__":
    add_user("mali2", "mali2@fsu.edu")
    user = get_user("mali2")
    print(user["username"], user["email"])

    add_user_goals(1, 2000, 150, 50.00)
    goals = get_user_goals(1)
    print(goals["calorie_goal"], goals["protein_goal_g"], goals["budget_weekly"])

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
    