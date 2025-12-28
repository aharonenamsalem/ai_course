from crewai import Agent, Crew, Task, Process
from crewai.tools import BaseTool, tool

import os
from dotenv import load_dotenv
load_dotenv()
# from api_keys import openai
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


############### Tools

class MyCalcTool(BaseTool):
    name : str = "My Calculator Tool"
    description : str = "Use this tool to perform math operations"
    
    def _run(self, equation : str) -> str:
        return eval(equation)
        

@tool("My Calculator Tool",)
def my_calc_tool(equation : str) -> str:
    """ Use this tool to perform math operations """
    return eval(equation)

################### Agent 1


math_agent = Agent(
    role="Math Master",
    goal="You are able to evaluate math expressions",
    backstory="You are a math genius with a sense of humor",
    tools=[MyCalcTool()],
    verbose=True
    
)

task1 = Task(
    description="{equation}",
    expected_output="Give full details in bullet points",
    agent=math_agent
)

##################################### Agent 2


writer_agent = Agent(
    role='Writer',
    goal="Craft compelling explanations based on the result of the math equations",
    backstory="""You are renowed content strategist, known for insightful and engaging
                articles. You transform complex concepts into compelling narratives.
                """,
    verbose=True,
)

task2 = Task(
    description="Using the insights provided, explain in great detail how the equation and result formed",
    expected_output="Explain in great detail, save the result in markdown. Do not add the triple tick marks at the begining or the end of the file.",
    output_file="math.md",
    agent=writer_agent,
    
)


# ################# Crew

crew = Crew(
    agents=[math_agent, writer_agent],
    tasks=[task1, task2],
    verbose=True,
    process=Process.sequential
)



math_input = input("Enter math expression: ")

result = crew.kickoff(inputs={'equation': math_input })
print('##############################################################')
print(result)