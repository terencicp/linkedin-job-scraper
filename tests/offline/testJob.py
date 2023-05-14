import os
import unittest
from scraper.LinkedIn import LinkedIn
from scraper.Job import Job
from selenium.webdriver.common.by import By


class TestJob(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.linkedin = LinkedIn(requests_per_minute=100)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mock_job_page = os.path.join('file://' + current_dir, 'job.html')
        cls.job = Job(mock_job_page)

    def test_title_element_found(self):
        title_element = self.locate_element(By.CLASS_NAME, self.job.TITLE_CLASS)
        self.assertIsNotNone(title_element)

    def test_company_element_found(self):
        company_element = self.locate_element(By.CLASS_NAME, self.job.COMPANY_CLASS)
        self.assertIsNotNone(company_element)

    def test_description_element_found(self):
        description_element = self.locate_element(By.ID, self.job.DESCRIPTION_ID)
        self.assertIsNotNone(description_element)

    def test_details_element_found(self):
        details_element = self.locate_element(By.CLASS_NAME, self.job.DETAILS_CLASS)
        self.assertIsNotNone(details_element)

    def test_sector_element_found(self):
        sector_element = self.locate_element(By.CSS_SELECTOR, self.job.SECTOR_CSS)
        self.assertIsNotNone(sector_element)

    def locate_element(self, locator, value):
        return self.linkedin.webpage.find_element(locator, value)
