import time
from urllib.parse import quote

from .exceptions import MissingDependencyError
from .schemas import LinkedInCredentials, LinkedInProfile


class LinkedInBot:
    def __init__(self, credentials: LinkedInCredentials, headless: bool = False):
        self.credentials = credentials
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def login(self) -> None:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise MissingDependencyError(
                "Playwright is not installed. Install with `pip install linkedin-autobot[automation]`."
            ) from exc

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        self.page.goto("https://www.linkedin.com/login")
        self.page.fill("input#username", self.credentials.email)
        self.page.fill("input#password", self.credentials.password)
        self.page.click("button[type='submit']")
        time.sleep(5)

    def visit_profile(self, profile_url: str) -> None:
        self.page.goto(profile_url)
        time.sleep(3)

    def find_profile_url_by_name(self, name: str) -> str:
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={quote(name)}"
        self.page.goto(search_url)
        time.sleep(4)

        selectors = [
            "a[href*='/in/']",
            ".entity-result__title-text a",
            ".linked-area[href*='/in/']",
        ]

        for selector in selectors:
            try:
                locator = self.page.locator(selector).first
                href = locator.get_attribute("href")
                if href and "/in/" in href:
                    return href.split("?")[0]
            except Exception:
                continue

        raise ValueError(f"Could not find a LinkedIn profile for '{name}'.")

    def _safe_text(self, selector: str) -> str:
        try:
            locator = self.page.locator(selector).first
            if locator.count() == 0:
                return ""
            return " ".join(locator.inner_text().strip().split())
        except Exception:
            return ""

    def _first_text(self, selectors: list[str]) -> str:
        for selector in selectors:
            value = self._safe_text(selector)
            if value:
                return value
        return ""

    def collect_profile(self, profile_url: str) -> LinkedInProfile:
        self.visit_profile(profile_url)

        return LinkedInProfile(
            profile_url=profile_url,
            full_name=self._first_text(["h1"]),
            title=self._first_text(
                [
                    "div.text-body-medium.break-words",
                    ".pv-text-details__left-panel .text-body-medium",
                    ".text-body-medium",
                ]
            ),
            location=self._first_text(
                [
                    ".pv-text-details__left-panel .text-body-small.inline",
                    ".text-body-small.inline.t-black--light.break-words",
                    ".text-body-small.inline",
                ]
            ),
            about=self._first_text(
                [
                    "section.artdeco-card:has(#about) div.inline-show-more-text",
                    "section.artdeco-card:has(#about) .full-width[dir='ltr']",
                    "#about ~ div .inline-show-more-text",
                    "#about ~ *",
                ]
            ),
            experience=self._first_text(
                [
                    "section.artdeco-card:has(#experience) .pvs-list__outer-container",
                    "#experience ~ div .pvs-list__outer-container",
                    "#experience ~ *",
                ]
            ),
        )

    def collect_profile_by_name(self, name: str) -> LinkedInProfile:
        profile = self.collect_profile(self.find_profile_url_by_name(name))
        if not profile.full_name:
            profile.full_name = name
        return profile

    def send_connection_request(self, profile_url: str, message: str | None = None) -> bool:
        self.visit_profile(profile_url)
        try:
            self.page.click("button[aria-label^='Connect']")
            time.sleep(1)
            if message:
                self.page.click("button[aria-label='Add a note']")
                self.page.fill("textarea[name='message']", message)
            self.page.click("button[aria-label='Send now']")
            return True
        except Exception:
            return False

    def close(self) -> None:
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
