import time
import urllib.parse
from scraper.LinkedIn import LinkedIn
from selenium.webdriver.common.by import By


class Search(LinkedIn):

    RESULTS_CLASS = 'jobs-search-results-list'
    PAGE_BUTTON_CLASS = 'artdeco-pagination__indicator'
    LINK_CLASS = 'job-card-list__title'

    def __init__(self, query):
        super().__init__()
        self.keywords = query['keywords']
        self.location = query['location']
        self.page_number = 1
        self.search()

    def search(self):
        url = ('https://www.linkedin.com/jobs/search/?refresh=true' +
               '&keywords=' + urllib.parse.quote(self.keywords) +
               '&location=' + urllib.parse.quote(self.location) +
               '&start=' + str((self.page_number - 1) * 25))
        self.go_to(url)

    def scroll_to_bottom(self):
        time.sleep(3)
        results = LinkedIn.webpage.find_element(By.CLASS_NAME, self.RESULTS_CLASS)
        LinkedIn.webpage.execute_script('arguments[0].scrollTop += 5000;', results)

    def page_range(self):
        self.scroll_to_bottom()
        buttons = LinkedIn.webpage.find_elements(By.CLASS_NAME, self.PAGE_BUTTON_CLASS)
        page_numbers = [int(button.text) for button in buttons if button.text.isdigit()]
        page_count = max(page_numbers)
        return range(1, page_count + 1)

    def go_to_page(self, new_page_number):
        if new_page_number is not self.page_number:
            self.page_number = new_page_number
            self.search()

    def get_urls(self):
        anchors = LinkedIn.webpage.find_elements(By.CLASS_NAME, self.LINK_CLASS)
        urls = [self.remove_query(a) for a in anchors]
        return urls

    @staticmethod
    def remove_query(a):
        url = a.get_attribute('href')
        url_without_query_string = url.split('?')[0]
        return url_without_query_string
