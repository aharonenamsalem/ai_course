import os
from secret_keys import openai
os.environ["OPENAI_API_KEY"] = openai

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
model = ChatOpenAI(temperature=1.0, model="gpt-4o")


chat_prompt_template = ChatPromptTemplate.from_messages(
    [
     ('system', 'you are a 8th class student that he is good i math and programming'),
     ('ai', 'Here is the code that you wanted'),
     ('human', '{input}')
    ]
)

test_the_code_template = ChatPromptTemplate.from_messages(
    [
     ('system', 'you are a professional in math and python programming'),
     ('ai', 'Here is the test results'),
     ('human', 'please run unit test on this python code {code}')
    ]
)



from langchain_core.output_parsers import StrOutputParser

chain_code= chat_prompt_template | model | StrOutputParser() 
chain_tests = test_the_code_template | model | StrOutputParser()
result = chain_code | chain_tests | {
    "name": chain_code,
    "items": chain_tests,
}

response = result.invoke(input="give me a code in python measure the Area of a Rectangle given the length of its side")
print(response)