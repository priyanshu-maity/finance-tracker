import undetected_chromedriver as uc
from dotenv import load_dotenv
import os
import yaml


class BStatScraper:
    def __init__(self, headless=True):
        options = uc.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        self.driver = uc.Chrome(options=options)

    def scrape(self, url):
        self.driver.get(url)
        customer_id, password = self.load_details()
        selectors = self.load_selectors()

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