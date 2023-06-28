import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LinkedIn:
    """
    The LinkedIn class encapsulates functionality to interact with the website.
    It provides methods to navigate, login, and limit the number of requests.
    """

    EMAIL_ID = 'username'
    PASSWORD_ID = 'password'
    SIGN_IN_BUTTON_XPATH = '//button[@type="submit"]'

    webpage = webdriver.Chrome(service=Service('/driver/chrome'))
    rate_limit = None

    def __init__(self, requests_per_minute=1):
        """
        Initialize the LinkedIn class with a specified rate limit for requests.

        Parameters:
        requests_per_minute (int): The number of requests to allow per minute.
        """
        if LinkedIn.rate_limit is None:
            LinkedIn.rate_limit = 60 / requests_per_minute

    def go_to(self, url):
        """
        Navigate to a specified URL and wait for the page to load.

        Parameters:
        url (str): The URL to navigate to.
        """
        LinkedIn.webpage.get(url)
        self.wait_for_page_to_load(url)
        time.sleep(self.rate_limit)

    def wait_for_page_to_load(self, url):
        """
        Wait for a page to load. If the page does not load within 10 seconds,
        an attempt is made to reload it.

        Parameters:
        url (str): The URL of the page to wait for.
        """
        wait = WebDriverWait(self.webpage, 10)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
        except TimeoutException as e:
            print(f"The page could not be loaded: {e}")
            self.go_to(url)

    def login(self, login):
        """
        Login to LinkedIn using the provided credentials.

        Parameters:
        login (dict): A dictionary containing 'email' and 'password' keys.
        """
        self.go_to('https://www.linkedin.com/login')
        page = LinkedIn.webpage
        page.find_element(By.ID, self.EMAIL_ID).send_keys(login['email'])
        page.find_element(By.ID, self.PASSWORD_ID).send_keys(login['password'])
        page.find_element(By.XPATH, self.SIGN_IN_BUTTON_XPATH).click()

    def close(self):
        """
        End the browser session.
        """
        self.webpage.quit()
