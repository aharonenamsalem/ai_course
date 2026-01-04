import os
from secret_keys import openai
os.environ["OPENAI_API_KEY"] = openai

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
model = ChatOpenAI(temperature=1.0, model="gpt-4o")


prompt_template_name = PromptTemplate(
    input_variables=["cuisine"],
    template="I want to open a fancy resaurant for {cuisine} food. Suggest ONE fancy name for it, return only the name, no comments or remarks.",
)

prompt_template_items = PromptTemplate(
    input_variables=["restaurant_name"],
    template="Suggest some menu items for {restaurant_name}. Return it as a comma separated list. no comments or remarks.",
)

from langchain_core.output_parsers import StrOutputParser

chain_name = prompt_template_name | model | StrOutputParser()
chain_items = prompt_template_items | model | StrOutputParser()

result = chain_name | chain_items | {
    "name": chain_name,
    "items": chain_items,
}

response = result.invoke("Italian")
print(response["name"])
print(response["items"])