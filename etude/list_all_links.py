import json

lines = open("crawl_data/nishio.jsonl").readlines()
pages = [json.loads(line) for line in lines]
links = set()
for page in pages:
    links.update(page["links"])
