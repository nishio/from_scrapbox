"""
generate scaffolds (link structure only) from jsonl
"""
import json
from tqdm import tqdm

new_pages = {}
project = "nishio"
data = json.load(open(f"{project}.json"))
title_map = json.load(open("title_map.json"))
all_links = json.load(open(f"crawl_data/{project}/all_links.json"))
for page in tqdm(data["pages"]):
    new_page = {}
    title = page["title"]
    if isinstance(page["lines"][0], str):
        lines = page["lines"]
    else:
        lines = [line["text"] for line in page["lines"]]

    if title.startswith("🌀"):
        continue

    if "[ja.icon]" in lines:
        continue

    if "[en.icon]" in lines:
        # copy original
        new_page["lines"] = page["lines"]
        new_page["title"] = title
        new_pages[title] = new_page
        continue

    text = "\n".join(lines)
    links = [k for k in all_links if f"[{k}]" in text]

    new_title = title_map.get(title, title)
    if new_title in new_pages:
        # raise ValueError(f"{new_title} already exists")
        print(f"{new_title} already exists, title: {title}")
        continue

    new_lines = [new_title, "/".join(f"[{title_map.get(k, k)}]" for k in links)]
    new_pages[new_title] = {"title": new_title, "lines": new_lines}

# convert new_pages dict to list
new_pages = list(new_pages.values())
new_data = {"pages": new_pages}
json.dump(new_data, open("scaffolds.json", "w"), ensure_ascii=False, indent=2)
