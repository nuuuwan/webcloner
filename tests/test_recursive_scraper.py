import unittest

from webcloner import RecursiveScraper


class TestCase(unittest.TestCase):
    def test_scrape(self):
        rs = RecursiveScraper("https://dmmc.lk", 10)
        rs.scrape()
