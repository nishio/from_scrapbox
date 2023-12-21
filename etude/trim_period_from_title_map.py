import json

count = 0
links = json.load(open("title_map.json"))
for k in links:
    if links[k].endswith("."):
        print(links[k])
        count += 1
        links[k] = links[k][:-1]

json.dump(links, open("title_map.json", "w"), ensure_ascii=False, indent=2)
