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

cuisine_input = input("Enter a cuisine type: ")
template_prompt = prompt_template_name.format(cuisine=cuisine_input)



response = model.invoke(template_prompt)

print(response.content)

