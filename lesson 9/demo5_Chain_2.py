import os
from secret_keys import openai
os.environ["OPENAI_API_KEY"] = openai

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

model = ChatOpenAI(temperature=1.0, model="gpt-4o")


prompt_template = ChatPromptTemplate.from_messages(
    [
        ('system', 'You are a comedian who tells jokes about {topic}'),
        ('human', 'Tell me {joke_count} jokes')
    ]
)
chain = prompt_template | model | StrOutputParser()
response = chain.invoke({'topic': "Lawyers", 'joke_count': 3})
print(response)