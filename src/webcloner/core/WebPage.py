import os

import requests
from bs4 import BeautifulSoup, Comment
from utils import File, Hash, Log

log = Log("WebPage")


class WebPage:
    TAGS_RED_LIST = {
        "script",
        "style",
        "link",
        "meta",
    }
    ATTRIBUTES_GREEN_LIST = {"href", "src", "alt"}

    def __init__(self, url):
        self.url = url

    @property
    def hash(self) -> str:
        SALT = "webcloner-v1"
        return Hash.md5(self.url + SALT)

    @property
    def domain(self) -> str:
        return self.url.split("//")[-1].split("/")[0].replace(".", "-")

    @property
    def data_dir(self) -> str:
        data_dir = os.path.join("data", self.domain, "original", self.hash[:8])
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        return data_dir

    @property
    def raw_html_path(self) -> str:
        return os.path.join(self.data_dir, "raw.html")

    def scrape(self):
        response = requests.get(self.url)
        response.raise_for_status()
        with open(self.raw_html_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        size = os.path.getsize(self.raw_html_path)
        log.info(f'Scraped "{self.url}" to {self.raw_html_path} ({size}B)')

    @property
    def reduced_html_path(self):
        return os.path.join(self.data_dir, "reduced.html")

    def reduce_elem(self, elem):
        # Remove HTML comments
        for comment in elem.find_all(
            string=lambda text: isinstance(text, Comment)
        ):
            comment.extract()

        for tag in elem.find_all(True):  # Find all tags in the element
            if tag.name in self.TAGS_RED_LIST:
                tag.decompose()  # Remove the tag if it's in the ignored list
            else:
                # Ensure tag.attrs is not None before processing
                if tag.attrs:
                    tag.attrs = {
                        key: value
                        for key, value in tag.attrs.items()
                        if key in self.ATTRIBUTES_GREEN_LIST
                    }
                # Strip and collapse all whitespace inside the tag
                if tag.string:
                    tag.string.replace_with(" ".join(tag.string.split()))

                # Remove tags with no text and no attributes
                if not tag.attrs and not tag.get_text(strip=True):
                    tag.decompose()
        return elem

    def reduce_html(self):
        html = File(self.raw_html_path).read()
        soup = BeautifulSoup(html, "html.parser")
        reduced_soup = self.reduce_elem(soup)
        reduced_html = str(reduced_soup)

        # Remove empty lines
        reduced_html = "\n".join(
            line for line in reduced_html.splitlines() if line.strip()
        )

        File(self.reduced_html_path).write(reduced_html)
        size = os.path.getsize(self.reduced_html_path)
        log.info(f"Wrote {self.reduced_html_path} ({size}B)")

    @property
    def txt_path(self):
        return os.path.join(self.data_dir, "text.txt")

    def extract_text(self):
        reduced_html = File(self.reduced_html_path).read()
        soup = BeautifulSoup(reduced_html, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        text = "\n".join(line for line in text.splitlines() if line.strip())
        File(self.txt_path).write(text)
        size = os.path.getsize(self.txt_path)
        log.info(f"Wrote {self.txt_path} ({size}B)")

    @property
    def simple_md_path(self):
        return os.path.join(self.data_dir, "simple.md")

    def convert_to_simple_markdown(self):
        reduced_html = File(self.reduced_html_path).read()
        soup = BeautifulSoup(reduced_html, "html.parser")

        # Convert links to markdown format
        for a_tag in soup.find_all("a", href=True):
            link_text = a_tag.get_text(strip=True)
            a_tag.replace_with(f"[{link_text}]({a_tag['href']})")

        # Extract plain text with markdown links
        markdown_text = soup.get_text(separator="\n", strip=True)
        markdown_text = "\n\n".join(
            line for line in markdown_text.splitlines() if line.strip()
        )

        File(self.simple_md_path).write(markdown_text)
        size = os.path.getsize(self.simple_md_path)
        log.info(f"Wrote {self.simple_md_path} ({size}B)")

    @property
    def link_list(self):
        soup = BeautifulSoup(File(self.reduced_html_path).read(), "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            link = a_tag["href"]
            if link.startswith("http"):
                links.add(link)
        return list(sorted(links))
