import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class CalcSeleniumTest(unittest.TestCase):
    def setUp(self):
        # Automatically download and manage ChromeDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get("https://www.calculator.net/")
        time.sleep(2)  # wait for page to load

    def tearDown(self):
        self.driver.quit()

    def calculate(self, num1, operator, num2):
        driver = self.driver
        
        # Click numbers and operators on calculator.net
        driver.find_element(By.XPATH, f"//span[text()='{num1}']").click()
        
        if operator == '+':
            driver.find_element(By.XPATH, "//span[text()='+']").click()
        elif operator == '*':
            driver.find_element(By.XPATH, "//span[text()='×']").click()
        elif operator == '-':
            driver.find_element(By.XPATH, "//span[text()='-']").click()
        elif operator == '/':
            driver.find_element(By.XPATH, "//span[text()='÷']").click()
            
        driver.find_element(By.XPATH, f"//span[text()='{num2}']").click()
        driver.find_element(By.XPATH, "//span[text()='=']").click()
        
        time.sleep(1)
        result = driver.find_element(By.ID, "sciOutPut").text
        return result

    def test_addition(self):
        result = self.calculate(2, "+", 3)
        self.assertIn("5", result)

    def test_subtraction(self):
        result = self.calculate(5, "-", 2)
        self.assertIn("3", result)

    def test_multiplication(self):
        result = self.calculate(4, "*", 3)
        self.assertIn("12", result)

    def test_division(self):
        result = self.calculate(8, "/", 2)
        self.assertIn("4", result)

    def test_simple_calculation(self):
        result = self.calculate(1, "+", 1)
        self.assertIn("2", result)

if __name__ == "__main__":
    unittest.main()