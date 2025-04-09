from bs4 import BeautifulSoup
from utils import Log

log = Log("HTML2MD")


class HTML2MD:
    def convert(self, html_str: str) -> list[str]:
        root = BeautifulSoup(html_str, "html.parser")
        return self.convert_elem(root)

    def clean(self, s: str) -> str:
        return s.strip()

    def convert_str_element(self, elem) -> list[str]:
        s = self.clean(elem)
        if not s:
            return None
        return [s]

    def convert_tagged_elem(self, elem) -> list[str]:
        s = self.clean(elem.get_text())
        if elem.name == "h1":
            return ["# " + s]
        if elem.name == "p":
            return [s]
        return None

    def convert_parent_elem(self, elem) -> list[str]:
        md_lines = []
        for child in elem.children:
            child_md_lines = self.convert_elem(child)
            if child_md_lines:
                md_lines.extend(child_md_lines)
        return md_lines

    def convert_elem(self, elem) -> list[str]:
        if isinstance(elem, str):
            return self.convert_str_element(elem)

        return self.convert_tagged_elem(elem) or self.convert_parent_elem(
            elem
        )
