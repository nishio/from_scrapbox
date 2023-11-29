import json
nishio_user_id = "582e63d27c56960011aff09e"
pages = []

for line in open('crawl_data/villagepump.jsonl'):
    pages.append(json.loads(line))

def find_me():
    for p in pages:
        for line in p["lines"]:
            if line["text"] == "[nishio.icon]":
                print(line["userId"])
                break

num_pages = 0
num_my_pages = 0
num_pages_with_me = 0

num_lines = 0
num_my_lines = 0
for p in pages:
    num_pages += 1
    if p["user"]["id"] == nishio_user_id:
        num_my_pages += 1
    if any(x["id"] == nishio_user_id for x in p["collaborators"]):
        num_pages_with_me += 1
    for line in p["lines"]:
        num_lines += 1
        if line["userId"] == nishio_user_id:
            num_my_lines += 1

print("num_pages", num_pages, "num_my_pages", num_my_pages, "num_pages_with_me", num_pages_with_me)
print("num_lines", num_lines, "num_my_lines", num_my_lines)

"""
Result:
num_pages 22977 num_my_pages 1342 num_pages_with_me 1989
num_lines 740316 num_my_lines 65458
"""