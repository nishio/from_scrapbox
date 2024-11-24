"""
translate from jsonl file
"""

import json
from tqdm import tqdm
import os
from utils.lang import contains_japanese_characters
from tasks.translate import bashi, simple_translate

project = "nishio"
all_links = json.load(open(f"crawl_data/{project}/all_links.json"))
title_map_file = "./title_map.json"
title_map = json.load(open(title_map_file))

lines = open(f"crawl_data/{project}.jsonl").readlines()
pages = [json.loads(line) for line in lines]

# sort by modified time
pages = list(sorted(pages, key=lambda x: x["updated"], reverse=True))

# for the first time, translate all pages
# errors may occur, so save result every time
translation_file = "translation.json"
if os.path.exists(translation_file):
    translation = json.load(open("translation.json"))
else:
    translation = {}


error_file = "error.json"
if os.path.exists(error_file):
    error = json.load(open(error_file))
else:
    error = {}


def get_missing_links(text, translated_text, links):
    missing_links = []
    for k in links:
        if f"[{k}]" in text and f"[{title_map.get(k, k)}]" not in translated_text:
            missing_links.append(k)
    return missing_links


for page in tqdm(pages):
    ja_title = page["title"]
    if ja_title in translation:
        # already translated, skip for first iteration
        print("SKIP:", ja_title, "already translated")
        continue

    if ja_title in error:
        # already translated, skip for first iteration
        print("SKIP:", ja_title, "already translated")
        continue

    if ja_title in title_map:
        en_title = title_map[ja_title]
    elif not contains_japanese_characters(ja_title):
        en_title = ja_title
    else:
        en_title = simple_translate.main(ja_title)
        title_map[ja_title] = en_title
        json.dump(title_map, open(title_map_file, "w"), ensure_ascii=False, indent=2)

    lines = [line["text"] for line in page["lines"]]
    if ja_title.startswith("🌀"):
        continue

    if "[ja.icon]" in lines:
        print("SKIP:", ja_title, "has ja icon")
        continue

    if "[en.icon]" in lines:
        # copy original afterward
        print("SKIP:", ja_title, "has en icon")
        continue

    text = "\n".join(lines)
    links = [k for k in all_links if f"[{k}]" in text]
    # This should be all_links, not title_map.keys()
    # Reason: the goal is to keep links between pages. They are sometimes in English.

    print(links)
    try:
        new_text = bashi.translate(text)
    except Exception as e:
        error[ja_title] = str(e)
        json.dump(error, open(error_file, "w"), ensure_ascii=False, indent=2)
        continue

    print("-" * 10)
    print(text)
    print("-" * 10)
    print(new_text)
    # check if the number of lines are the same
    new_lines = new_text.splitlines()
    if len(lines) == len(new_lines):
        # same number of lines
        for i in range(len(lines)):
            missing_links = get_missing_links(lines[i], new_lines[i], links)
            if len(missing_links) > 0:
                print(f"Missing links: {missing_links}")
                print(f"Original: {lines[i]}")
                print(f"Translated: {new_lines[i]}")
                new_lines[i] += "  [missinglink.icon]" + "/".join(
                    f"[{title_map.get(k, k)}]" for k in missing_links
                )
                print()
        new_text = "\n".join(new_lines)
    else:
        print("The number of lines are different.")
        # split into chunks by blank lines
        chunks = text.split("\n\n")
        new_chunks = new_text.split("\n\n")
        if len(chunks) == len(new_chunks):
            for i in range(len(chunks)):
                missing_links = get_missing_links(chunks[i], new_chunks[i], links)
                if len(missing_links) > 0:
                    print(f"Missing links: {missing_links}")
                    print(f"Original: {chunks[i]}")
                    print(f"Translated: {new_chunks[i]}")
                    new_chunks[i] += "\n[missinglink.icon]" + "/".join(
                        f"[{title_map.get(k, k)}]" for k in missing_links
                    )
                    print()
            new_text = "\n\n".join(new_chunks)
        else:
            print("The number of chunks are different.")
            missing_links = get_missing_links(text, new_text, links)
            if len(missing_links) > 0:
                print(f"Missing links: {missing_links}")
                new_text += "\n[missinglink.icon]" + "/".join(
                    f"[{title_map.get(k, k)}]" for k in missing_links
                )
                print()

    print("-" * 10)
    print(new_text)
    print("-" * 10)

    translation[ja_title] = new_text
    json.dump(translation, open(translation_file, "w"), ensure_ascii=False, indent=2)


# for the update, translate only new pages
def foo():
    translation = json.load(open("translation.json"))
    pages = []
    for ja_title in translation:
        lines = translation[ja_title].splitlines()
        title = title_map.get(ja_title, ja_title)
        if lines[0] != title:
            lines.insert(0, title)
        pages.append(
            {
                "title": title,
                "lines": lines,
            }
        )
    json.dump(
        {"pages": pages}, open("translation_for_scrapbox.json", "w"), ensure_ascii=False
    )
