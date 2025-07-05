from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from contextlib import contextmanager
from typing import Generator, Optional

class BaseScraper:
    def __init__(
        self,
        storage_state: Optional[str] = None,
        cookies: Optional[list[dict]] = None,
        user_agent: Optional[str] = None,
        proxy: Optional[dict] = None,
        headless: bool = False,
    ):
        """
        Args:
            storage_state (str): Path to storage state JSON file.
            cookies (list[dict]): List of cookies to set (ignored if storage_state is used).
            user_agent (str): User agent string to spoof.
            proxy (dict): Proxy config like {'server': 'http://...', 'username': '...', 'password': '...'}.
            headless (bool): Whether to launch browser in headless mode.
        """
        self.storage_state = storage_state
        self.cookies = cookies
        self.user_agent = user_agent
        self.proxy = proxy
        self.headless = headless

        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    @contextmanager
    def launch(self) -> Generator[Page, None, None]:
        with sync_playwright() as p:
            browser_args = {"headless": self.headless}

            if self.proxy:
                browser_args["proxy"] = self.proxy

            self.browser = p.chromium.launch(**browser_args)

            context_args = {}

            if self.storage_state:
                context_args["storage_state"] = self.storage_state

            if self.user_agent:
                context_args["user_agent"] = self.user_agent

            self.context = self.browser.new_context(**context_args)

            # Set cookies manually only if storage_state is not provided
            if self.cookies and not self.storage_state:
                self.context.add_cookies(self.cookies)

            self.page = self.context.new_page()
            try:
                yield self.page
            finally:
                self.context.close()
                self.browser.close()

    def run(self):
        with self.launch() as page:
            self.scrape(page)

    def scrape(self, page: Page):
        raise NotImplementedError("Subclasses must implement the scrape() method.")
