import os
import unittest
from scraper.LinkedIn import LinkedIn
from scraper.Search import Search


class TestSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        query = {
            'keywords': "data analyst",
            'location': "European union"
        }
        cls.linkedin = LinkedIn(requests_per_minute=100)
        cls.search = Search(query)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cls.mock_search_page = os.path.join('file://' + current_dir, 'search.html')

    def test_search_count_pages(self):
        self.linkedin.go_to(self.mock_search_page)
        self.assertEqual(self.search.page_range(), range(1, 41))

    def test_search_get_urls(self):
        self.linkedin.go_to(self.mock_search_page)
        urls = self.search.get_urls()
        self.assertTrue('/jobs/view/' in urls[0])

