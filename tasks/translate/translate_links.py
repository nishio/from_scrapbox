from . import simple_translate
import json
from tqdm import tqdm
from utils.lang import contains_japanese_characters

title_map_file = "title_map.json"


def _generate_initial_title_map():
    """was used to generate title_map.json
    It translates all page titles in nishio.json to English.
    However, currently I use a different approach to translate titles.
    (Translate all links in crawl_data/nishio/all_links.json)
    """
    data = json.load(open(in_file, "r"))
    titles = [page["title"] for page in data["pages"]]
    print(len(titles))
    print(len([t for t in titles if contains_japanese_characters(t)]))
    titles.sort()

    title_map = {}
    for title in tqdm(titles):
        if not contains_japanese_characters(title):
            continue
        en_title = simple_translate.main(title)
        title_map[title] = en_title

    json.dump(title_map, open(title_map_file, "w"), ensure_ascii=False, indent=2)


def stat1():
    # title occurence count
    data = json.load(open(in_file, "r"))
    titles = [page["title"] for page in data["pages"]]
    from collections import defaultdict

    count = defaultdict(int)
    for p in tqdm(data["pages"]):
        text = "\n".join(p["lines"])
        for title in titles:
            # count[title] += text.count(title)
            if title in text:
                count[title] += 1

    buf = [(v, k) for (k, v) in count.items()]
    buf.sort(reverse=True)


def stat2():
    # title occurence count
    data = json.load(open(in_file, "r"))
    titles = [page["title"] for page in data["pages"]]
    from collections import defaultdict

    count = defaultdict(int)
    for p in tqdm(data["pages"]):
        text = "\n".join(p["lines"])
        for title in titles:
            # count[title] += text.count(title)
            if title in text:
                count[p["title"]] += 1

    buf = [(v, k) for (k, v) in count.items()]
    buf.sort(reverse=True)

    buf2 = [(v, k) for (v, k) in buf if all(c not in k for c in "🌀🤖")]


def update_title_map():
    lines = open("crawl_data/nishio.jsonl").readlines()
    pages = [json.loads(line) for line in lines]
    links = set()
    for page in pages:
        links.update(page["links"])

    title_map = json.load(open(title_map_file))

    print(f"check {len(links)} links")
    to_translate = []
    for link in links:
        if link in title_map:
            continue
        if not contains_japanese_characters(link):
            continue
        to_translate.append(link)

    print(f"translate {len(to_translate)} links")
    for link in tqdm(to_translate):
        en_link = simple_translate.main(link)
        title_map[link] = en_link

    json.dump(title_map, open(title_map_file, "w"), ensure_ascii=False, indent=2)


update_title_map()
