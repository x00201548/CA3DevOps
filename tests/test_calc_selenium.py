import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class CalcSeleniumTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")  
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get("https://www.calculator.net/")
        time.sleep(2)  # wait for page to load

    def tearDown(self):
        self.driver.quit()

    def click_buttons(self, buttons):
        """Click a sequence of buttons on the calculator"""
        for b in buttons:
            self.driver.find_element(By.XPATH, f"//span[text()='{b}']").click()
            time.sleep(0.2)  # tiny pause between clicks
        self.driver.find_element(By.XPATH, "//span[text()='=']").click()
        time.sleep(0.5)
        return self.driver.find_element(By.ID, "sciOutPut").text.strip()

    def test_addition(self):
        result = self.click_buttons(["2", "+", "3"])
        self.assertIn("5", result)

    def test_subtraction(self):
        result = self.click_buttons(["5", "-", "2"])
        self.assertIn("3", result)

    def test_subtraction(self):
        result = self.click_buttons(["3", "-", "2"])
        self.assertIn("1", result)


if __name__ == "__main__":
    unittest.main()
