import unittest
from validators import validateDays, validateMeals, validateEmail, validateWeight, validateAge, validateSex, validateBudget, validateCalories, validateAllergens

class TestInputs(unittest.TestCase):
    def test_validateMeals(self):
        self.assertEqual(validateMeals("breakfast, lunch"), (True, ["breakfast", "lunch"]))
        