import os
import unittest

from webcloner import WebPage

TEST_WEBPAGE = WebPage("https://dmmc.lk")


class TestCase(unittest.TestCase):
    def test_hash(self):
        self.assertEqual(
            TEST_WEBPAGE.hash, "6311967cab21d9d4481f797dbc5928be"
        )

    def test_scrape(self):
        TEST_WEBPAGE.scrape()
        self.assertTrue(os.path.exists(TEST_WEBPAGE.raw_html_path))
