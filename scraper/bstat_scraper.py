import undetected_chromedriver as uc
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from dotenv import load_dotenv
import os
import yaml
from time import sleep
import random


class BStatScraper:
    def __init__(self, headless=True):
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        if headless:
            options.add_argument('--headless')
        self.driver = uc.Chrome(options=options)

    def scrape(self, url):
        self.driver.get(url)
        customer_id, password = self.load_details()
        selectors = self.load_selectors()

        sleep(5)
        self.driver.switch_to.frame(0)

        customer_id_input: WebElement = WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, selectors['customer_id']))
        )
        self.smart_type(customer_id_input, customer_id)
        sleep(random.uniform(1.5, 3.0))

        WebDriverWait(self.driver, timeout=10).until(
            EC.element_to_be_clickable((By.XPATH, selectors['continue_button']))
        ).click()
        sleep(random.uniform(1.5, 3.0))

        self.driver.switch_to.default_content()

        password_input: WebElement = WebDriverWait(self.driver, timeout=20).until(
            EC.element_to_be_clickable((By.XPATH, selectors['password']))
        )
        self.smart_type(password_input, password)
        sleep(random.uniform(1.5, 3.0))

        WebDriverWait(self.driver, timeout=10).until(
            EC.element_to_be_clickable((By.XPATH, selectors['login_button']))
        ).click()

    def close(self):
        self.driver.quit()

    @staticmethod
    def load_details() -> tuple[str, str]:
        load_dotenv()
        return os.getenv('CUSTOMER_ID'), os.getenv('PASSWORD')

    @staticmethod
    def load_selectors() -> dict:
        with open('selectors.yaml', 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def smart_type(element: WebElement, text: str, min_delay: float = 0.05, max_delay: float = 0.5):
        for char in text:
            element.send_keys(char)
            sleep(random.uniform(min_delay, max_delay))

if __name__ == '__main__':
    scraper = BStatScraper(headless=False)
    try:
        scraper.scrape('https://netbanking.hdfcbank.com/netbanking/')
    finally:
        scraper.close()