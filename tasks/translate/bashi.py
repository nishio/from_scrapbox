"""
Bashi is a translator
"""
import openai
import dotenv
import os
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain.schema.messages import SystemMessage

dotenv.load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

llm_model = "gpt-3.5-turbo"
llm = ChatOpenAI(temperature=0, model=llm_model)

SYSTEM_PROMPT = open("tasks/translate/BASHI_PROMPT.txt").read()
title_map = json.load(open("title_map.json"))
# It is OK, no need to use all_links.
# Reason: it is for hint for translation. all_links includes English links. It is too much.


def translate(text):
    jaen = {k: v for k, v in title_map.items() if f"[{k}]" in text}
    filled_prompt = SYSTEM_PROMPT.replace(
        "{mapping}", json.dumps(jaen, ensure_ascii=False)
    )
    bashi_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=(filled_prompt)),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )
    # print(bashi_template.format_messages(text=text))
    r = llm(bashi_template.format_messages(text=text))
    return r.content


if __name__ == "__main__":
    print(translate("[西尾 泰和]"))  # [NISHIO Hirokazu]
