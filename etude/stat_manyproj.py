import os
import json
import re
from tqdm import tqdm

v0 = [f for f in os.listdir("crawl_data") if f.endswith(".jsonl")]
# print(v0)
import re


def stat1():
    stat = []
    for f in tqdm(v0):
        # print(f)
        lines = open(f"crawl_data/{f}").readlines()
        stat.append((len(lines), f.split(".")[0]))
    stat.sort(reverse=True)
    json.dump(stat, open("stat1.json", "w"), indent=2)


from collections import defaultdict

stat = defaultdict(int)
for f in tqdm(v0):
    # print(f)
    lines = open(f"crawl_data/{f}").readlines()
    for line in lines:
        data = json.loads(line)
        if not "lines" in data:
            continue
        text = "\n".join([x["text"] for x in data["lines"]])
        for x in re.findall("\[/[^]]+\]", text):
            stat[x] += 1

stat = [(stat[k], k) for k in stat if k[2] != " " if not k.endswith(".icon]")]
stat2 = [x for x in stat if not k.endswith(".icon]")]
stat.sort(reverse=True)
json.dump(stat, open("stat2.json", "w"), indent=2, ensure_ascii=False)
