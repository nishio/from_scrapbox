"""
Find many projects to crawl
"""

import os
import json
import re

v0 = [f for f in os.listdir("crawl_data") if f.endswith(".jsonl")]


v1 = {}
from string import ascii_letters, digits

OK_CAHRS = ascii_letters + digits + "-"

for f in v0:
    print(f)
    for line in open(f"crawl_data/{f}").readlines():
        page = json.loads(line)
        for line in page["lines"]:
            bracket_contents = re.findall("\[/(.*?)\]", line["text"])
            external_link_proj = [
                x.split("/")[0]
                for x in bracket_contents
                if x and x[0] not in ' *,$"#()-.^\\_{}[]'
            ]
            for p in external_link_proj:
                if all(c in OK_CAHRS for c in p):
                    v1[p.lower()] = p
    print(v1)

v0 = [f.split(".")[0] for f in v0]
v1 = list(v1.values()) + v0
v1.sort()
json.dump(v1, open("projects.json", "w"), indent=2)
