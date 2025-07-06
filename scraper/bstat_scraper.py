import undetected_chromedriver as uc


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