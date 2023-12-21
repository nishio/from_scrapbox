import json
from utils.lang import contains_japanese_characters

all_links = json.load(open("crawl_data/nishio/all_links.json"))
title_map = json.load(open("title_map.json"))
data = json.load(open("nishio.json"))
output = {}

num_collision = 0
for page in data["pages"]:
    title = page["title"]
    lines = page["lines"]
    if not isinstance(lines[0], str):
        lines = [line["text"] for line in lines]

    if contains_japanese_characters(title):
        new_title = title_map.get(title, title)
    else:
        new_title = title

    if title.startswith("🌀"):
        continue

    if "[ja.icon]" in lines:
        # print("ja icon", title)
        continue

    if new_title in output:
        print(f"[{new_title}]: [{title}] / [{output[new_title]}]")
        num_collision += 1
    else:
        output[new_title] = title

print("num collision", num_collision)
