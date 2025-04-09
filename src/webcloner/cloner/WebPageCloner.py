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
        for data_dir in os.listdir(self.data_domain_dir):
            simple_md_path = os.path.join(
                self.data_domain_dir, data_dir, "simple.md"
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
    def site_map_path(self):
        return os.path.join(self.data_domain_dir, "site_map.md")

    def gen_site_map(self):

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        md_content = File(self.combined_md_path).read()
        messages = [
            {
                "role": "user",
                "content": "\n".join(
                    [
                        md_content,
                        "",
                        "Generate a site map for the above content.",
                        "DO NOT include any comments, or preambles.",
                    ]
                ),
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )

        site_map = response.choices[0].message.content.strip()
        File(self.site_map_path).write(site_map)
        size = os.path.getsize(self.site_map_path)
        log.info(f"Wrote {self.site_map_path} ({size}B)")
