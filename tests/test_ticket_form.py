import unittest
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class FormCompletion(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_full_form_completion(self):
        driver = self.driver

        # URL to get
        driver.get("http://localhost:5000")

        assert "Support Ticket" in driver.title

        # grab all input elements
        f_name = driver.find_element_by_id("f_name")
        l_name = driver.find_element_by_id("l_name")
        email = driver.find_element_by_id("email")
        p_number = driver.find_element_by_id("phone_number")
        issue = Select(driver.find_element_by_id("ticket_type"))
        severity = Select(driver.find_element_by_id("severity"))
        msg = driver.find_element_by_xpath('//*[@id="message"]')

        # send input text
        f_name.send_keys("Selenium")
        f_name.send_keys(Keys.TAB)

        l_name.send_keys("Python")
        l_name.send_keys(Keys.TAB)

        email.send_keys("seleniumtest@gmail.com")
        email.send_keys(Keys.TAB)

        p_number.send_keys("6507876895")
        p_number.send_keys(Keys.TAB)

        issue.select_by_value("106")  # there are values from 101 - 110 (102 = maps)
        severity.select_by_value("P3")  # there are vales from P3 - P1 (P3 = priority)

        msg.send_keys("Testing this first selenium test script")
        msg.send_keys(Keys.TAB)

        # save a screenshot of the filled out form
        driver.save_screenshot(os.path.join(os.getcwd(), 'screenshot.png'))

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
