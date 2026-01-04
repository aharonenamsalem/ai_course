import os
from secret_keys import openai
os.environ["OPENAI_API_KEY"] = openai

from langchain_openai import ChatOpenAI

model = ChatOpenAI(temperature=1.0, model="gpt-4o")

response = model.invoke("I want to open a fancy restaurant for Italian food. Suggest a fancy name for it")

print(response.content)

