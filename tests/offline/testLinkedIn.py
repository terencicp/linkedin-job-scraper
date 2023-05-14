import os
import unittest
from scraper.LinkedIn import LinkedIn
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class TestLinkedIn(unittest.TestCase):

    def setUp(self):
        self.linkedin = LinkedIn(requests_per_minute=100)

    def test_single_selenium_driver_instance(self):
        l2 = LinkedIn()
        self.assertEqual(LinkedIn.webpage, l2.webpage)

    def test_single_rate_limit(self):
        l2 = LinkedIn(requests_per_minute=5)
        self.assertEqual(LinkedIn.rate_limit, l2.rate_limit)

    def test_login_form_elements_found(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mock_login_page = os.path.join('file://' + current_dir, 'login.html')
        self.linkedin.go_to(mock_login_page)
        try:
            email_field = LinkedIn.webpage.find_element(By.ID, LinkedIn.EMAIL_ID)
            password_field = LinkedIn.webpage.find_element(By.ID, LinkedIn.PASSWORD_ID)
            sign_in_button = LinkedIn.webpage.find_element(By.XPATH, LinkedIn.SIGN_IN_BUTTON_XPATH)
            self.assertIsNotNone(email_field)
            self.assertIsNotNone(password_field)
            self.assertIsNotNone(sign_in_button)
        except NoSuchElementException as ex:
            self.fail(f"Login elements not found: {ex}")
