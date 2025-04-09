import os
import unittest

from webcloner import WebPageCloner


class TestCase(unittest.TestCase):
    def test_webpage_cloner(self):
        wpc = WebPageCloner(os.path.join("data", "dmmc-lk"))
        wpc.combine_simple_markdown()
        self.assertTrue(os.path.exists(wpc.combined_md_path))
