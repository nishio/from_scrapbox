import concurrent.futures
import requests
import json
import os
import re
from tqdm import tqdm
from time import sleep, perf_counter
import dotenv

import openai
import dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

from . import simple_translate
from utils.lang import contains_japanese_characters

dotenv.load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

llm_model = "gpt-3.5-turbo"
llm = ChatOpenAI(temperature=0, model=llm_model)

SYSTEM_PROMPT = open("tasks/translate/BASHI_PROMPT.txt").read().replace("\n", "")
bashi_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=(SYSTEM_PROMPT)),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)


def call_gpt(text):
    r = llm(bashi_template.format_messages(text=text))
    return r.content


FOOTER = """
This page is auto-translated from [/nishio/{ja_title}] using GPT-3.5.
""".replace(
    "\n", ""
)

NO_TRANS_FOOTER = """
This page is written in English by NISHIO Hirokazu and copied from [/nishio/{ja_title}].
""".replace(
    "\n", ""
)


in_file = "./nishio.json"
out_file = "./en_local.json"
title_map_file = "./title_map.json"


def generate_line(text):
    return {
        "text": text,
        "created": 946652400,  # 2000-01-01 00:00:00
        "updated": 946652400,
        "userId": "582e63d27c56960011aff09e",  # nishio
    }


def translate_links(text):
    global cache
    # print(text)
    keywords = re.findall("\[(.*?)\]", text)
    # print(keywords)
    for k in keywords:
        en = cache.get(k)
        if en:  # translation exists
            text = text.replace(f"[{k}]", f" [{en}] ")
    # print(text)
    return text


def to_english(text):
    if body not in cache:
        if not contains_japanese_characters(body):
            return text

        no_cache += len(bytes(body, "utf-8"))
        en = call_deepl(body)
        cache[body] = en
        is_updated = True

    return prefix + cache[body] + postfix


def translate_one_page(page):
    """
    translate one page without metadata, update page destructively

    """
    ja_title = page["title"]
    if ja_title in title_map:
        en_title = title_map[ja_title]
    else:
        en_title = simple_translate.main(ja_title)
        title_map[ja_title] = en_title
        json.dump(title_map, open(title_map_file, "w"), ensure_ascii=False, indent=2)

    page["title"] = en_title

    def translate_line(line):
        tl_text = translate_links(line["text"])
        en_text = to_english(tl_text)
        return {"text": en_text}

    has_toplevel_en = False
    target_lines = []
    for line in page["lines"]:
        if "[en.icon]" == line["text"].strip():
            has_toplevel_en = True
        if "[enjabelow.icon]" in line["text"]:
            # skip following lines
            break
        target_lines.append(line)

    if has_toplevel_en:
        # no need to translate
        page["lines"].extend(
            [
                generate_line("---"),
                generate_line(NO_TRANS_FOOTER.format(ja_title=ja_title)),
            ]
        )
        return

    contents = "\n".join([line["text"] for line in target_lines])
    translated_contents = call_gpt(contents)
    translated_lines = translated_contents.split("\n")
    if len(target_lines) != len(translated_lines):
        print(
            "length mismatch",
            ja_title,
            en_title,
            len(target_lines),
            len(translated_lines),
        )

    new_lines = []
    # 翻訳された行を元のリストに戻す
    for i, translated_line in enumerate(translated_lines):
        page["lines"][i].update(translated_line)

    page["lines"].extend(
        [
            generate_line("---"),
            generate_line(FOOTER.format(ja_title=ja_title)),
        ]
    )


def translate_pages(pages):
    for page in tqdm(pages):
        translate_one_page(page)  # update destructively


def translate_from_json_to_json():
    start_time = perf_counter()
    in_file = "./data.json"
    data = json.load(open(in_file, "r"))

    # sort page by its updated time
    pages = list(sorted(data["pages"], key=lambda x: x["updated"], reverse=True))

    translate_pages(pages)  # update pages(and data) destructively
    json.dump(data, open("./data_en.json", "w"), ensure_ascii=False, indent=2)
    print("translate:", perf_counter() - start_time)


def translate_keywords():
    global total, no_cache, cache
    start_time = perf_counter()
    cache_data = "./cache.json"
    cache = json.load(open(cache_data, "r"))
    total = 0
    no_cache = 0

    in_file = "./keywords.json"
    data = json.load(open(in_file, "r"))

    print(len(data))
    for kw in tqdm(data):
        # print(kw, to_english(kw))
        to_english(kw)

    with open(cache_data, "w") as file:
        json.dump(cache, file, ensure_ascii=False, indent=2)

    print("total", total, "no_cache", no_cache, "ratio", no_cache / total)
    print("translate:", perf_counter() - start_time)


def main():
    translate_from_json_to_json()


def local_trial_10pages():
    print("running local trial")
    data = json.load(open(in_file, "r"))

    # sort page by its updated time
    pages = list(sorted(data["pages"], key=lambda x: x["updated"], reverse=True))[:10]
    data["pages"] = pages  # to omit other pages

    translate_pages(pages)  # update pages(and data) destructively
    json.dump(data, open(out_file, "w"), ensure_ascii=False, indent=2)


# if __name__ == "__main__":
#     # to avoid trials on local environment break CI on GitHub Actions
#     if os.environ.get("GITHUB_ACTIONS") == "true":
#         main()
#     else:
#         print("Not running within a GitHub Actions environment")
#         # main()
#         local_trial_10pages()
#         # translate_keywords()


def find_occurence(text, mapping):
    occur = {}
    for k, v in mapping.items():
        if k in text:
            occur[k] = v
    return occur


def generate_initial_title_map():
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


def add_link_to_title_map():
    lines = open("crawl_data/nishio.jsonl").readlines()
    pages = [json.loads(line) for line in lines]
    links = set()
    for page in pages:
        links.update(page["links"])

    title_map = json.load(open(title_map_file))

    for link in tqdm(links):
        if link in title_map:
            continue
        if not contains_japanese_characters(link):
            continue
        en_link = simple_translate.main(link)
        title_map[link] = en_link

    json.dump(title_map, open(title_map_file, "w"), ensure_ascii=False, indent=2)
