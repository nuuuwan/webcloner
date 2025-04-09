import os

import requests  # Added for HTTP requests
from utils import Hash, Log

log = Log("WebPage")


class WebPage:
    def __init__(self, url):
        self.url = url

    @property
    def hash(self) -> str:
        SALT = "webcloner-v1"
        return Hash.md5(self.url + SALT)

    @property
    def raw_html_path(self) -> str:
        return os.path.join("data", "raw_html", self.hash + ".html")

    def scrape(self):
        response = requests.get(self.url)
        response.raise_for_status()
        with open(self.raw_html_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        size = os.path.getsize(self.raw_html_path)
        log.info(f"Scraped {self.url} to {self.raw_html_path} ({size}B)")
