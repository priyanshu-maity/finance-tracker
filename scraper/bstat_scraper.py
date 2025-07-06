import undetected_chromedriver as uc
from dotenv import load_dotenv
import os


class BStatScraper:
    def __init__(self, headless=True):
        options = uc.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        self.driver = uc.Chrome(options=options)

    def scrape(self, url):
        self.driver.get(url)
        ...

    def close(self):
        self.driver.quit()
    
    @staticmethod
    def load_details(self) -> tuple[str, str]:
        load_dotenv()
        return os.getenv('CUSTOMER_ID'), os.getenv('PASSWORD')