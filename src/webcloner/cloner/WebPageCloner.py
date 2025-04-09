import os

from openai import OpenAI
from utils import File, Log

log = Log("WebPageCloner")


class WebPageCloner:
    def __init__(self, data_domain_dir):
        self.data_domain_dir = data_domain_dir

    @property
    def combined_md_path(self):
        return os.path.join(self.data_domain_dir, "combined.md")

    def combine_simple_markdown(self):
        all_md_lines = []
        data_original_dir = os.path.join(
            self.data_domain_dir,
            "original",
        )
        for data_dir in os.listdir(data_original_dir):
            simple_md_path = os.path.join(
                data_original_dir, data_dir, "simple.md"
            )
            if not os.path.exists(simple_md_path):
                continue

            all_md_lines.append(f"# {data_dir}")
            child_md_lines = File(simple_md_path).read_lines()
            for child_md_line in child_md_lines:
                if child_md_line not in all_md_lines:
                    all_md_lines.append(child_md_line)

        File(self.combined_md_path).write_lines(all_md_lines)
        size = os.path.getsize(self.combined_md_path)
        log.info(f"Wrote {self.combined_md_path} ({size}B)")

    @property
    def readme_path(self):
        return os.path.join(self.data_domain_dir, "README.md")

    def gen_site_map(self):

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        md_content = File(self.combined_md_path).read()
        messages = [
            {
                "role": "system",
                "content": "\n".join(
                    [
                        "Generate a README containing the most ",
                        " useful information of the website.",
                        "Start with a short about section.",
                        "Then, PRIORITIZE the links users most want,"
                        " like contact, online services, other services,",
                        " and information, at the top.",
                        "",
                        "DO use markdown headings appropriately.",
                        "DO NOT include any comments, or preambles.",
                        "DO NOT use begin and end quotes.",
                        "---",
                    ]
                ),
            },
            {
                "role": "user",
                "content": md_content,
            },
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )

        site_map = response.choices[0].message.content.strip()
        File(self.readme_path).write(site_map)
        size = os.path.getsize(self.readme_path)
        log.info(f"Wrote {self.readme_path} ({size}B)")
