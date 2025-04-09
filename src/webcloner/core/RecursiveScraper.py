from webcloner.core.WebPage import WebPage


class RecursiveScraper:
    def __init__(self, start_url, max_pages):
        self.start_url = start_url
        self.max_pages = max_pages

    def scrape(self):
        visited = set()
        to_visit = [self.start_url]

        while to_visit and len(visited) < self.max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue
            if self.start_url not in url:
                continue

            visited.add(url)
            i = len(visited)
            print(f"{i}/{self.max_pages}) Scraping: {url}")

            webpage = WebPage(url)
            webpage.scrape()
            webpage.reduce_html()
            webpage.extract_text()
            webpage.convert_to_simple_markdown()

            link_list = webpage.link_list
            to_visit.extend(link for link in link_list if link not in visited)
