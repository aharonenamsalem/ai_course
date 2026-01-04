import os
from secret_keys import openai
os.environ["OPENAI_API_KEY"] = openai

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
model = ChatOpenAI(temperature=1.0, model="gpt-4o")


chat_prompt_template = ChatPromptTemplate.from_messages(
    [
     ('system', 'You are a helpful AI assistant with a sense of humor.'),
     ('human', 'Hi How are you?'),
     ('ai', 'I am good. How can I help you?'),
     ('human', '{input}')
    ]
)
template = chat_prompt_template.format_messages(input="What is the capital of South Africa?")
response = model.invoke(template)
print(response.content)










