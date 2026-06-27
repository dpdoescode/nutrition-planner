# 🥗 Nutrition Planner CLI

A command-line nutrition planning app that generates personalized 7-day meal plans based on your health goals, dietary restrictions, and weekly budget.

---

## 🚀 Features

- **Personalized Meal Plans** — 7-day plans tailored to your calorie goal, allergens, and meal preferences
- **Nutrient Tracking** — tracks calories, protein, calcium, iron, potassium, and vitamin C per meal
- **Allergen Filtering** — filters recipes based on your dietary restrictions
- **Smart Grocery Pricing** — estimates weekly cost using real ingredient data via Spoonacular
- **Budget Tracking** — compares estimated weekly cost against your set budget
- **User Profiles** — saves your goals and allergens to a local SQLite database
- **Recipe Caching** — minimizes API calls by caching recipes per meal type

---

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Database:** SQLite (via `sqlite3`)
- **APIs:** Edamam Recipe Search API, Spoonacular API
- **Libraries:** `requests`, `json`, `datetime`, `random`, `os`

---

## 📁 File Structure
nutrition-planner/

├── main.py          # Entry point — user flow, recipe fetching, display

├── queries.py       # All database operations

├── models.py        # Table creation

├── database.py      # SQLite connection

├── validators.py    # Input validation functions

└── README.md

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/dpdoescode/nutrition-planner.git
cd nutrition-planner
```

### 2. Install dependencies

```bash
pip install requests
```

### 3. Set up the database

```bash
python3 models.py
```

### 4. Set your API keys

```bash
export MEALPLAN_API="your_edamam_api_key"
export SPOONACULAR_API="your_spoonacular_api_key"
```

> ⚠️ You need to re-export these every time you open a new terminal session.

---

## 🔑 API Keys

### Edamam Recipe Search API
- Sign up at [developer.edamam.com](https://developer.edamam.com)
- Create an app under **Recipe Search API**
- You'll get an `app_id` and `app_key`
- The `app_id` is hardcoded in `main.py` — the `app_key` is loaded from `MEALPLAN_API`

### Spoonacular API
- Sign up at [spoonacular.com/food-api](https://spoonacular.com/food-api)
- Get your API key from the dashboard
- Loaded from `SPOONACULAR_API` environment variable

---

## 🧪 Running the App

```bash
python3 main.py
```

You'll be prompted to:
1. Enter a username (login or create a profile)
2. Set your calorie goal, weight, age, sex, budget, and allergens (new users only)
3. Choose which meals to include (breakfast, lunch, dinner, snack)
4. Wait while recipes are fetched and cached
5. View your 7-day meal plan with nutrients, estimated cost, and URLs

---

## 🗄️ Database Schema

| Table | Description |
|---|---|
| `users` | Stores username and email |
| `user_goals` | Stores calorie, protein, budget, and nutrient goals |
| `user_allergens` | Stores allergens per user |
| `user_meal_preferences` | Stores meal preferences per user |
| `meal_plans` | Stores generated meal plans with avg nutrients and cost |

---

## ⚠️ Notes

- The free tier of Edamam limits API requests per minute — the app handles this with automatic retries and sleep delays
- The database file (`nutrition_app.db`) is excluded from version control — run `python3 models.py` to recreate it
- Nutrient goals (protein, calcium, iron, potassium, vitamin C) are automatically calculated from your weight, age, and sex

---

## 👥 Contributors

- **Diego Perez-Aguilar** — [@dpdoescode](https://github.com/dpdoescode)
- **Malachi Davey** — [@malachidavey](https://github.com/malachidavey)