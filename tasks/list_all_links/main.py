"""
from crawled jsonl, get all links (including red links)
"""

import json

project = "nishio"
print("list all links in project", project)

lines = open(f"crawl_data/{project}.jsonl").readlines()
pages = [json.loads(line) for line in lines]
links = set()
for page in pages:
    links.update(page["links"])

json.dump(
    list(links),
    open(f"crawl_data/{project}/all_links.json", "w"),
    ensure_ascii=False,
    indent=2,
)

print(f"wrote all {len(links)} links to", f"crawl_data/{project}/all_links.json")
