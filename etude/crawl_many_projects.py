import subprocess
import json
from tqdm import tqdm
import retrying

cmd = "deno run --v8-flags=--max-old-space-size=16000 --allow-read --allow-net --allow-write tasks/crawl_scrapbox/index.ts --project".split()
projects = json.load(open("crawl_data/projects.json"))

# Some projects are skipped because of the following reasons:
# Fatal JavaScript out of memory: Reached heap limit
OUT_OF_MEMORY = [
    "TfTBenchmark",
    "argus-knowledge",
    "discordwiki",
    "emoji",
    "inajob-inline",
    "june29",
]


@retrying.retry(stop_max_attempt_number=3)
def crawl(p):
    subprocess.check_call(cmd + [p])


# for p in tqdm(projects):
#     print(p)
#     if p <= OUT_OF_MEMORY[-1]:
#         continue  # out of memory
#     crawl(p)

for p in tqdm(OUT_OF_MEMORY):
    print(p)
    crawl(p)
