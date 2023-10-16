import unittest
from selenium import webdriver
from PageObjects import HomePage

class Mail(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://google.com/")
        self.driver.maximize_window()

    def test_01_search(self):
        homepage = HomePage(self.driver)
        self.assertEquals(HomePage.get_page_title(), 'Google')

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()