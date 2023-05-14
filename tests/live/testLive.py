import unittest
import time
from scraper.LinkedIn import LinkedIn
from scraper.Search import Search
from scraper.Job import Job

class TestLive(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        credentials = {
            'email': "example@mail.com",
            'password': "DontHackMePlz"
        }
        cls.linkedin = LinkedIn(requests_per_minute=20)
        cls.linkedin.login(credentials)
        cls.query = {
            'keywords': "data analyst",
            'location': "European union"
        }

    def test_linkedin_login(self):
        self.linkedin.go_to('https://www.linkedin.com/login')
        time.sleep(3)
        feed_url = "https://www.linkedin.com/feed/"
        self.assertEqual(self.linkedin.webpage.current_url, feed_url)

    def test_search_count_pages(self):
        search = Search(self.query)
        self.assertEqual(search.page_range(), range(1, 41))

    def test_search_get_urls(self):
        search = Search(self.query)
        urls = search.get_urls()
        self.assertTrue(urls[0].startswith("https://www.linkedin.com/jobs"))

    def test_extract_html_elements(self):
        search = Search(self.query)
        urls = search.get_urls()
        job = Job(urls[0])
        self.assertTrue(job.extract_html_elements())

    @classmethod
    def tearDownClass(cls):
        cls.linkedin.close()
