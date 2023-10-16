"""
Credit for a vast majority of this page goes to this project: https://github.com/dbeley/rymscraper
"""

# =====================================
# Imports
# =====================================

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time


# =====================================
# Classes
# =====================================

class RymBrowser(webdriver.Firefox):

    USER_URL = "https://rateyourmusic.com/~{}"

    def __init__(self, headless=True):
        self.options = Options()
        if headless:
            self.options.add_argument('-headless')

        webdriver.Firefox.__init__(self, options=self.options)

    def __del__(self):
        self.quit()

    def restart(self):
        self.quit()
        webdriver.Firefox.__init__(self, options=self.options)

    def get_url(self, url):
        while True:
            self.get(str(url))
            class_to_click_on = [
                "as-oil__btn-optin",  # cookie bar
                "fc-cta-consent",  # consent popup
                # "ad-close-button",  # advertisement banner
            ]
            for i in class_to_click_on:
                if len(self.find_elements(By.CLASS_NAME, i)) > 0:
                    self.find_element(By.CLASS_NAME, i).click()

            if len(self.find_elements(By.CLASS_NAME, "disco_expand_section_link")) > 0:
                try:
                    for index, link in enumerate(
                        self.find_elements(By.CLASS_NAME, "disco_expand_section_link")
                    ):
                        self.execute_script(
                            f"document.getElementsByClassName('disco_expand_section_link')[{index}].scrollIntoView(true);"
                        )
                        link.click()
                        time.sleep(0.2)
                except Exception as e:
                    pass
            # Test if IP is banned.
            if self.is_ip_banned():
                self.quit()
                raise Exception("IP banned from rym. Can't do any requests to the website. Exiting.")
            # Test if browser is rate-limited.
            if self.is_rate_limited():
                self.restart()
            else:
                break
        return

    def get_page_source(self):
        return self.page_source

    def get_soup(self):
        return BeautifulSoup(self.page_source, "lxml")

    def is_ip_banned(self):
        return self.get_soup().title.text.strip() == "IP blocked"

    def is_rate_limited(self):
        return self.get_soup().find("form", {"id": "sec_verify"})

    def get_case_sensitive_username(self, username: str):
        """!
        @param username  case insenistive username of user
        @return  case sensitive version of username, necessary for certain rym links
        """
        self.get_url(self.USER_URL.format(username))
        redirect_url = self.current_url
        return redirect_url[redirect_url.rfind("~") + 1:]

