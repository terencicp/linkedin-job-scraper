import time
import urllib.parse
from scraper.LinkedIn import LinkedIn
from selenium.webdriver.common.by import By


class Search(LinkedIn):
    """
    The Search class inherits from the LinkedIn class and is used to perform
    job searches on LinkedIn based on provided search queries.
    """

    RESULTS_CLASS = 'jobs-search-results-list'
    PAGE_BUTTON_CLASS = 'artdeco-pagination__indicator'
    LINK_CLASS = 'job-card-list__title'

    def __init__(self, query):
        """
        Initialize the Search class with a search query.

        Parameters:
        query (dict): A dictionary containing search keywords and location.
        """
        super().__init__()
        self.keywords = query['keywords']
        self.location = query['location']
        self.page_number = 1
        self.search()

    def search(self):
        """
        Execute a job search on LinkedIn using the provided keywords and location,
        and go to the specified page of search results.
        """
        url = ('https://www.linkedin.com/jobs/search/?refresh=true' +
               '&keywords=' + urllib.parse.quote(self.keywords) +
               '&location=' + urllib.parse.quote(self.location) +
               '&start=' + str((self.page_number - 1) * 25))
        self.go_to(url)

    def scroll_to_bottom(self):
        """
        Scroll to the bottom of the search results page to ensure all search
        results are loaded.
        """
        time.sleep(3)
        results = LinkedIn.webpage.find_element(By.CLASS_NAME, self.RESULTS_CLASS)
        LinkedIn.webpage.execute_script('arguments[0].scrollTop += 5000;', results)

    def page_range(self):
        """
        Return a range object representing all the page numbers in the search results.

        Returns:
        range: A range object representing all the page numbers.
        """
        self.scroll_to_bottom()
        buttons = LinkedIn.webpage.find_elements(By.CLASS_NAME, self.PAGE_BUTTON_CLASS)
        page_numbers = [int(button.text) for button in buttons if button.text.isdigit()]
        page_count = max(page_numbers)
        return range(1, page_count + 1)

    def go_to_page(self, new_page_number):
        """
        Go to a specific page of the search results.

        Parameters:
        new_page_number (int): The number of the page to go to.
        """
        if new_page_number is not self.page_number:
            self.page_number = new_page_number
            self.search()

    def get_urls(self):
        """
        Extract the URLs of all job postings on the current search results page.

        Returns:
        list: A list of job posting URLs.
        """
        anchors = LinkedIn.webpage.find_elements(By.CLASS_NAME, self.LINK_CLASS)
        urls = [self.remove_query(a) for a in anchors]
        return urls

    @staticmethod
    def remove_query(a):
        """
        Remove the query string from a job posting URL.

        Parameters:
        a (WebElement): A WebElement representing a link to a job posting.

        Returns:
        str: The job posting URL without the query string.
        """
        url = a.get_attribute('href')
        url_without_query_string = url.split('?')[0]
        return url_without_query_string
