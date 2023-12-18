"""
Usage: python -m tasks.translate.cui_translate --url https://scrapbox.io/nishio/%E5%90%8C%E7%90%86%E5%BF%83
"""
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import openai
import dotenv
import os
import json

dotenv.load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo", verbose=True)

from langchain.chains import SimpleSequentialChain
from utils.read_scrapbox_page import read_page

url = "https://scrapbox.io/nishio/%E5%B1%A4%E7%8A%B6%E3%81%AB%E3%81%AA%E3%81%A3%E3%81%A6%E3%81%84%E3%82%8B%E7%9F%A5%E8%AD%98%E3%81%A8%E3%81%AE%E5%90%91%E3%81%8D%E5%90%88%E3%81%84%E6%96%B9"

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, default=url)

args = parser.parse_args()


page = read_page(args.url)
text = "\n".join([line["text"] for line in page["lines"]])

title_map = json.load(open("title_map.json"))
jaen = {k: v for k, v in title_map.items() if f"[{k}]" in text}


SYSTEM_PROMPT = open("tasks/translate/BASHI_PROMPT.txt").read()
SYSTEM_PROMPT = SYSTEM_PROMPT.replace("{mapping}", json.dumps(jaen))
bashi_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=(SYSTEM_PROMPT)),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)
chains = []
chains.append(LLMChain(llm=llm, prompt=bashi_template))
# chains.append(LLMChain(llm=llm, prompt=kai_template))
# chains.append(LLMChain(llm=llm, prompt=enja_template))


overall_simple_chain = SimpleSequentialChain(chains=chains, verbose=True)
result = overall_simple_chain.run(text)

# check link occurence

# check if the number of lines are the same
text_lines = text.splitlines()
result_lines = result.splitlines()
if len(text_lines) == len(result_lines):
    # same number of lines
    for i in range(len(text_lines)):
        missing_links = []
        for k in jaen:
            if (
                f"[{k}]" in text_lines[i]
                and f"[{jaen[k]}]".lower() not in result_lines[i].lower()
            ):
                missing_links.append(k)

        if len(missing_links) > 0:
            print(f"Missing links: {missing_links}")
            print(f"Original: {text_lines[i]}")
            print(f"Translated: {result_lines[i]}")
            result_lines[i] += "  [missinglink.icon]" + "/".join(
                f"[{jaen[k]}]" for k in missing_links
            )
            print()
else:
    print("The number of lines are different.")
    print(len(result.splitlines()), len(text.splitlines()))
# print(len(result.splitlines()), len(text.splitlines()))

# print(result.splitlines())
# print([[k for k in jaen if f"[{k}]" in line] for line in text.splitlines()])

print("\n".join(result_lines))
import pdb

pdb.set_trace()
import sys

sys.exit(0)


SYSTEM_PROMPT = open("tasks/translate/BASHI_PROMPT.txt").read()
bashi_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=(SYSTEM_PROMPT)),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

SYSTEM_PROMPT = open("tasks/translate/KAI_PROMPT.txt").read().replace("\n", "")
kai_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=(SYSTEM_PROMPT)),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

SYSTEM_PROMPT = "Translate to Janapese"
enja_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=(SYSTEM_PROMPT)),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)


def translate_url(url):
    page = read_page_from_scrapbox(url)
    text = "\n".join([line["text"] for line in page["lines"]])
    r = llm(chat_template.format_messages(text=text))
    return r.content


overall_simple_chain = SimpleSequentialChain(chains=chains, verbose=True)
overall_simple_chain.run(text)
