import os
import unittest

from webcloner import WebPage

TEST_WEBPAGE = WebPage("https://dmmc.lk")


class TestCase(unittest.TestCase):
    def test_hash(self):
        self.assertEqual(TEST_WEBPAGE.hash, "6311")

    def test_scrape(self):
        TEST_WEBPAGE.scrape()
        self.assertTrue(os.path.exists(TEST_WEBPAGE.raw_html_path))
        TEST_WEBPAGE.reduce_html()
        self.assertTrue(os.path.exists(TEST_WEBPAGE.reduced_html_path))
        TEST_WEBPAGE.extract_text()
        self.assertTrue(os.path.exists(TEST_WEBPAGE.txt_path))
        TEST_WEBPAGE.convert_to_simple_markdown()
        self.assertTrue(os.path.exists(TEST_WEBPAGE.simple_md_path))
