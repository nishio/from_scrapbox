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

dotenv.load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


SYSTEM_PROMPT = open("tasks/translate/BASHI_PROMPT.txt").read().replace("\n", "")
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

llm = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo", verbose=True)
# print(llm(chat_template.format_messages(text="こんにちは[世界]")))


# page = read_page_from_scrapbox(
#     "https://scrapbox.io/nishio/100%25%E5%89%8D%E3%81%AB%E9%80%B2%E3%82%80%E3%82%B3%E3%83%88%E3%82%92%E3%82%84%E3%82%8B"
# )

# text = "\n".join([line["text"] for line in page["lines"]])

# r = llm(chat_template.format_messages(text=text))

# print(r.content)


def translate_url(url):
    page = read_page_from_scrapbox(url)
    text = "\n".join([line["text"] for line in page["lines"]])
    r = llm(chat_template.format_messages(text=text))
    return r.content


from langchain.chains import SimpleSequentialChain
from utils.read_scrapbox_page import read_page

url = "https://scrapbox.io/nishio/Plurality%E3%81%A8%E3%82%B5%E3%82%A4%E3%83%9C%E3%82%A6%E3%82%BA"

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, default=url)

args = parser.parse_args()

chains = []
chains.append(LLMChain(llm=llm, prompt=bashi_template))
chains.append(LLMChain(llm=llm, prompt=kai_template))
chains.append(LLMChain(llm=llm, prompt=enja_template))

page = read_page(args.url)
text = "\n".join([line["text"] for line in page["lines"]])

overall_simple_chain = SimpleSequentialChain(chains=chains, verbose=True)
overall_simple_chain.run(text)
