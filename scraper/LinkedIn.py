import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LinkedIn:

    EMAIL_ID = 'username'
    PASSWORD_ID = 'password'
    SIGN_IN_BUTTON_XPATH = '//button[@type="submit"]'

    webpage = webdriver.Chrome(service=Service('/driver/chrome'))
    rate_limit = None

    def __init__(self, requests_per_minute=1):
        if LinkedIn.rate_limit is None:
            LinkedIn.rate_limit = 60 / requests_per_minute

    def go_to(self, url):
        LinkedIn.webpage.get(url)
        self.wait_for_page_to_load(url)
        time.sleep(self.rate_limit)

    def wait_for_page_to_load(self, url):
        wait = WebDriverWait(self.webpage, 10)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
        except TimeoutException as e:
            print(f"The page could not be loaded: {e}")
            self.go_to(url)

    def login(self, login):
        self.go_to('https://www.linkedin.com/login')
        page = LinkedIn.webpage
        page.find_element(By.ID, self.EMAIL_ID).send_keys(login['email'])
        page.find_element(By.ID, self.PASSWORD_ID).send_keys(login['password'])
        page.find_element(By.XPATH, self.SIGN_IN_BUTTON_XPATH).click()

    def close(self):
        self.webpage.quit()
