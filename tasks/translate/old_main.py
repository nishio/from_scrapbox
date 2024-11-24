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


def get_api_url(url):
    """
    >>> get_api_url("https://scrapbox.io/nishio/example")
    'https://scrapbox.io/api/pages/nishio/example'
    >>> get_api_url("https://scrapbox.io/api/pages/nishio/example")
    'https://scrapbox.io/api/pages/nishio/example'
    """
    import re

    if "api/pages/" in url:
        return url
    api_url = re.sub(
        r"(https://scrapbox\.io)/([^/]+)/([^/]+)", r"\1/api/pages/\2/\3", url
    )
    return api_url


def read_page_from_scrapbox(url):
    """
    url example: https://scrapbox.io/nishio/%F0%9F%A4%962023-08-13_07:08
    """
    import requests

    # if IS_PRIVATE_PROJECT:
    #     from read_private_project import read_private_pages

    #     page = read_private_pages(url)
    # else:
    #     api_url = get_api_url(url)
    #     page = requests.get(api_url).json()

    api_url = get_api_url(url)
    page = requests.get(api_url).json()

    return page


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

url = "https://scrapbox.io/nishio/%E3%83%8E%E3%82%A6%E3%82%A2%E3%82%B9%E3%83%95%E3%82%A3%E3%82%A2%E3%81%AE%E9%96%8B%E5%A2%BE%E3%81%A8%E4%BA%A4%E6%8F%9B%E6%A7%98%E5%BC%8F%E8%AB%96"
chains = []
chains.append(LLMChain(llm=llm, prompt=bashi_template))
chains.append(LLMChain(llm=llm, prompt=kai_template))
chains.append(LLMChain(llm=llm, prompt=enja_template))

page = read_page_from_scrapbox(url)
text = "\n".join([line["text"] for line in page["lines"]])

overall_simple_chain = SimpleSequentialChain(chains=chains, verbose=True)
overall_simple_chain.run(text)
