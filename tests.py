import unittest
from validators import validateDays, validateMeals, validateEmail, validateWeight, validateAge, validateSex, validateBudget, validateCalories, validateAllergens

class TestInputs(unittest.TestCase):
    def test_validateMeals(self):
        self.assertEqual(validateMeals("breakfast, lunch"), (True, ["breakfast", "lunch"]))

    def test_validateDays(self):
        self.assertTrue(validateDays("5"))
        self.assertFalse(validateDays("0"))
        self.assertFalse(validateDays("8"))

    def test_validateEmail(self):
        self.assertTrue(validateEmail("malachi@fsu.edu"))
        self.assertFalse(validateEmail("notanemail"))
        self.assertFalse(validateEmail("missing@domain"))
    
    def test_validateWeight(self):
        self.assertTrue(validateWeight("150"))
        self.assertFalse(validateWeight("49"))
        self.assertFalse(validateWeight("501"))

    def test_validateCalories(self):
        self.assertTrue(validateCalories("2000"))
        self.assertFalse(validateCalories("999"))
        self.assertFalse(validateCalories("3501"))
    
    def test_validateAge(self):
        self.assertTrue(validateAge("50"))
        self.assertFalse(validateAge("121"))
        self.assertFalse(validateAge("12"))
    
    def test_validateSex(self):
        self.assertTrue(validateSex("male"))
        self.assertTrue(validateSex("female"))
        self.assertFalse(validateSex("other"))
        self.assertFalse(validateSex(""))

    def test_validateBudget(self):
        self.assertTrue(validateBudget("50.00"))
        self.assertTrue(validateBudget("100"))
        self.assertFalse(validateBudget("-10"))
        self.assertFalse(validateBudget("abc"))
    
    def test_validateAllergens(self):
        is_valid, result = validateAllergens("gluten, dairy")
        self.assertTrue(is_valid)
        self.assertEqual(result, ["gluten", "dairy"])

        is_valid, result = validateAllergens("none")
        self.assertTrue(is_valid)
        self.assertEqual(result, [])

        is_valid, result = validateAllergens("gluten, chocolate")
        self.assertFalse(is_valid)
        self.assertIn("chocolate", result)

    
if __name__ == "__main__":
    unittest.main()

        