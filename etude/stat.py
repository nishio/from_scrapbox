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

def stat1():
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

def stat2():
    from collections import defaultdict
    ratio_stats = defaultdict(int)

    num_pages = 0

    for p in pages:
        num_pages += 1
        num_lines = 0
        num_my_lines = 0
        for line in p["lines"]:
            num_lines += 1
            if line["userId"] == nishio_user_id:
                num_my_lines += 1
        ratio = int(100 * num_my_lines / num_lines)
        ratio_stats[ratio] += 1

    print(ratio_stats)
    print([ratio_stats[i] for i in range(0, 101)])

    import matplotlib.pyplot as plt
    plt.plot([ratio_stats[i] for i in range(1, 101)])

def stat3():
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    x = []
    y = []

    for p in pages:
        num_lines = 0
        num_my_lines = 0
        for line in p["lines"]:
            num_lines += 1
            if line["userId"] == nishio_user_id:
                num_my_lines += 1
        if num_my_lines == 0:
            continue
        x.append(num_lines)
        y.append(num_my_lines)

    sns.jointplot(x=np.log10(x), y=np.log10(y), alpha=0.1, kind='scatter')
    plt.show()
    sns.jointplot(x=np.log10(x), y=np.log10(y), kind='kde')
    plt.show()


def stat4():
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    x = []
    y = []

    for p in pages:
        if p["title"].startswith("20"):
            continue
        num_lines = 0
        num_my_lines = 0
        for line in p["lines"]:
            num_lines += 1
            if line["userId"] == nishio_user_id:
                num_my_lines += 1
        if num_my_lines == 0:
            continue
        x.append(num_lines)
        y.append(num_my_lines / num_lines)

    sns.jointplot(x=np.log10(x), y=y, alpha=0.1, kind='scatter')
    plt.show()
    # sns.jointplot(x=np.log10(x), y=y, kind='kde')



is_user = []
is_collaborator = []
is_user_or_collaborator = []
is_in_icons = []
from collections import defaultdict
samples = defaultdict(list)
for p in pages:
    # is_user.append(p["user"]["id"] == nishio_user_id)
    # is_collaborator.append(any(x["id"] == nishio_user_id for x in p["collaborators"]))
    x = p["user"]["id"] == nishio_user_id or any(x["id"] == nishio_user_id for x in p["collaborators"])
    # is_user_or_collaborator.append(x)
    y = "nishio" in p["icons"]
    # is_in_icons.append(y)
    if x or y:
        samples[(x, y)].append(p["title"])

if 0:
    import pandas as pd
    pd.crosstab(is_user_or_collaborator, is_in_icons)
    """
    col_0  False  True 
    row_0              
    False  19155    491
    True     827   2504
    """

print("user or collaborator, but not in icons")
for v in samples[(True, False)][:10]:
    print(v)

print("in icons, but not user or collaborator")
for v in samples[(False, True)][:10]:
    print(v)
