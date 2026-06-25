import unittest
from validators import validateDays, validateMeals, validateEmail, validateWeight, validateAge, validateSex, validateBudget, validateCalories, validateAllergens

class TestInputs(unittest.TestCase):
    def test_validateMeals(self):
        self.assertEqual(validateMeals("breakfast, lunch"), (True, ["breakfast", "lunch"]))


    def test_validateEmail(self):
        self.assertTrue(validateEmail("malachi@fsu.edu"))
        self.assertFalse(validateEmail("notanemail"))
        self.assertFalse("missing@domain")
    
    def test_validateWeight(self):
        self.assertTrue(validateWeight("150"))
        self.assertFalse(validateWeight("49"))
        self.assertFalse(validateWeight("501"))

    def test_validateCalories(self):
        self.assertTrue(validateCalories("2000"))
        self.assertFalse(validateCalories("999"))
        self.assertFalse(validateCalories("3501"))
    
        