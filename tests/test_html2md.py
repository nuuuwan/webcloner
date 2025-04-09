import unittest

from webcloner import HTML2MD


class TestCase(unittest.TestCase):
    def test_convert(self):
        html_str = """
        <html>

            <body>
                <h1>Hello, World!</h1>
                <p>This is a test.</p>
            </body>"""
        md_lines = HTML2MD().convert(html_str)
        print(md_lines)
        expected_md_lines = [
            "# Hello, World!",
            "This is a test.",
        ]
        self.assertEqual(md_lines, expected_md_lines)
