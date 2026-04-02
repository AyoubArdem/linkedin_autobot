import time
from urllib.parse import quote

from playwright.sync_api import sync_playwright


class LinkedinBot:
    def __init__(self, email, password, full_name=None):
        self.full_name = full_name
        self.password = password
        self.email = email
        self.playwright = None
        self.browser = None
        self.page = None

    def login(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.goto("https://www.linkedin.com/login")
        self.page.fill("input#username", self.email)
        self.page.fill("input#password", self.password)
        self.page.click("button[type='submit']")
        time.sleep(5)
        print("Logged in")

    def visit_profile(self, profile_url):
        self.page.goto(profile_url)
        time.sleep(3)
        print(f"Visited {profile_url}")

    def find_profile_url_by_name(self, name):
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

    def _safe_text(self, selector):
        try:
            locator = self.page.locator(selector).first
            if locator.count() == 0:
                return ""
            return locator.inner_text().strip()
        except Exception:
            return ""

    def _first_text(self, selectors):
        for selector in selectors:
            value = self._safe_text(selector)
            if value:
                return " ".join(value.split())
        return ""

    def collect_data(self, profile_url):
        self.visit_profile(profile_url=profile_url)

        title = self._first_text(
            [
                "div.text-body-medium.break-words",
                ".pv-text-details__left-panel .text-body-medium",
                ".text-body-medium",
            ]
        )
        location = self._first_text(
            [
                ".pv-text-details__left-panel .text-body-small.inline",
                ".text-body-small.inline.t-black--light.break-words",
                ".text-body-small.inline",
            ]
        )
        about = self._first_text(
            [
                "section.artdeco-card:has(#about) div.display-flex.ph5.pv3 div.inline-show-more-text",
                "section.artdeco-card:has(#about) .full-width[dir='ltr']",
                "#about ~ div .inline-show-more-text",
                "#about ~ *",
            ]
        )
        experience = self._first_text(
            [
                "section.artdeco-card:has(#experience) li .display-flex.align-items-center.mr1.t-bold span[aria-hidden='true']",
                "section.artdeco-card:has(#experience) .pvs-list__outer-container",
                "#experience ~ div .pvs-list__outer-container",
                "#experience ~ *",
            ]
        )

        return {
            "title": title,
            "location": location,
            "about": about,
            "experience": experience,
        }

    def collect_data_by_name(self, name):
        profile_url = self.find_profile_url_by_name(name)
        data = self.collect_data(profile_url)
        data["profile_url"] = profile_url
        return data

    def send_connection_request(self, profile_url, message=None):
        self.visit_profile(profile_url)
        try:
            self.page.click("button[aria-label^='Connect']")
            time.sleep(1)
            if message:
                self.page.click("button[aria-label='Add a note']")
                self.page.fill("textarea[name='message']", message)
                self.page.click("button[aria-label='Send now']")
            else:
                self.page.click("button[aria-label='Send now']")
            print(f"Connection sent to {profile_url}")
            return True
        except Exception as exc:
            print(f"Failed to connect to {profile_url}: {exc}")
            return False

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("Browser closed")
