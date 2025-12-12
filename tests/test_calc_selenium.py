import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class CalcSeleniumTest(unittest.TestCase):
    def setUp(self):
        # Automatically download and manage ChromeDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("http://127.0.0.1:5000/calculator")
        self.driver.maximize_window()
        time.sleep(1)  # small wait for page to load

    def tearDown(self):
        self.driver.quit()

    def calculate(self, num1, num2, operator):
        driver = self.driver
        driver.find_element(By.NAME, "num1").clear()
        driver.find_element(By.NAME, "num1").send_keys(str(num1))

        driver.find_element(By.NAME, "operator").send_keys(operator)

        driver.find_element(By.NAME, "num2").clear()
        driver.find_element(By.NAME, "num2").send_keys(str(num2))

        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(0.5)  # wait for result

        # return result text
        try:
            result = driver.find_element(By.XPATH, "//p[contains(text(),'Result')]").text
        except:
            result = driver.find_element(By.XPATH, "//p[contains(@style,'color:red')]").text
        return result

    def test_addition(self):
        result = self.calculate(5, 3, "+")
        self.assertIn("8", result)

    def test_subtraction(self):
        result = self.calculate(10, 4, "-")
        self.assertIn("6", result)

    def test_multiplication(self):
        result = self.calculate(6, 7, "*")
        self.assertIn("42", result)

    def test_division(self):
        result = self.calculate(20, 5, "/")
        self.assertIn("4", result)

    def test_divide_by_zero(self):
        result = self.calculate(10, 0, "/")
        self.assertIn("Cannot divide by zero", result)

if __name__ == "__main__":
    unittest.main()