import time
from scraper.LinkedIn import LinkedIn
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class Job(LinkedIn):
    """
    The Job class inherits from the LinkedIn class and is used to extract
    job-specific details from a given LinkedIn job URL.
    """

    TITLE_CLASS = 'jobs-unified-top-card__job-title'
    DETAILS_CLASS = 'job-details-job-alert__description'
    COMPANY_CLASS = 'jobs-unified-top-card__company-name'
    SECTOR_CSS = '.t-14.mt5'
    DESCRIPTION_ID = 'job-details'

    def __init__(self, url):
        """
        Initialize the Job class with a job URL.

        Parameters:
        url (str): The URL of the job posting on LinkedIn.
        """
        super().__init__()
        self.url = url
        self.go_to(url)
        self.load_dynamic_content()
        if self.extract_html_elements():
            self.extract_text_from_html_elements()

    def as_dict(self):
        """
        Returns the job details as a dictionary.

        Returns:
        dict: A dictionary containing the job details if they were successfully
        extracted, or an empty dictionary if not.
        """
        if hasattr(self, 'id'):
            return {
                'id': self.id,
                'title': self.title,
                'location': self.location,
                'company': self.company,
                'sector': self.sector,
                'job title': self.job_title,
                'description': self.description,
            }
        else:
            return {}

    def load_dynamic_content(self):
        """
        Load dynamic content on the job page by executing JavaScript to click
        the "see more" button.
        """
        click_description_button_js = '''
            let seeMoreButton = document.querySelector('button.artdeco-card__action');
            if (seeMoreButton) seeMoreButton.click();
        '''
        self.webpage.execute_script(click_description_button_js)
        self.scroll_down()
        time.sleep(3)

    def scroll_down(self):
        """
        Scroll down the page by using the PAGE_DOWN key on the body of the page.
        """
        self.webpage.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

    def extract_html_elements(self):
        """
        Extract HTML elements containing job details from the webpage. If any
        required element is missing, the job is skipped.

        Returns:
        bool: True if all elements were successfully extracted, False otherwise.
        """
        page = LinkedIn.webpage
        try:
            self.title_element = page.find_element(By.CLASS_NAME, self.TITLE_CLASS)
            self.company_element = page.find_element(By.CLASS_NAME, self.COMPANY_CLASS)
            self.description_element = page.find_element(By.ID, self.DESCRIPTION_ID)
            self.details_element = page.find_element(By.CLASS_NAME, self.DETAILS_CLASS)
            self.sector_element = page.find_element(By.CSS_SELECTOR, self.SECTOR_CSS)
            return True
        except NoSuchElementException:
            print("Skipping job listing with missing data...")
            return False

    def extract_text_from_html_elements(self):
        """
        Extract text from the HTML elements that contain job details.
        """
        self.title = self.title_element.text
        self.company = self.company_element.text
        # Extract ID from URL: 'http://www.linkedin.com/jobs/view/3597550681'
        self.id = self.url.split('/')[5]
        # Remove text from the element's children (spans)
        sector_element_text = self.sector_element.text
        child_text = self.sector_element.find_element(By.TAG_NAME, 'span').text
        self.sector = sector_element_text.split(child_text)[0]
        # Remove 'About the job' from the start of the string
        self.description = self.description_element.text[13:].strip()
        # Location may have multiple parts: 'Barcelona, Catalonia, Spain'
        details = self.details_element.text.split(', ')
        self.job_title = details[0]
        self.location = ', '.join(details[1:])
