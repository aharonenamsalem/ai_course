from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from crewai_tools import FileReadTool
from langchain_experimental.utilities import PythonREPL

import os
from dotenv import load_dotenv
load_dotenv()
# from api_keys import openai
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# Tool 1: execute arbitrary Python code (used by the executor agent)
@tool("repl")
def repl(code: str) -> str:
    """Execute the provided Python code string and return its stdout.
    Useful for the Executor agent to run the analysis code."""
    return PythonREPL().run(command=code)

# Tool 2: read files (used by the coder agent to inspect CSV input)
file_read_tool = FileReadTool()

# --- Agent and Crew Definition ---

def run_crew(file_name: str, analysis_task: str):
    # 1. Create the Agents
    coder = Agent(
        role='Python Data Analyst',
        goal='Write python code to analyze data from a CSV file',
        backstory='You are an experienced data analyst who writes clear and efficient Python code.',
        tools=[file_read_tool],
        verbose=True,
        allow_delegation=False
    )

    executor = Agent(
        role='Python Executor',
        goal='Execute python code and return the result',
        backstory='You are a python execution environment capable of running code and capturing output.',
        tools=[repl],
        verbose=True,
        allow_delegation=False
    )

    # 2. Create the Tasks
    coding_task = Task(
        description=f'Write a python script to perform the following analysis: {analysis_task}. '
                    f'The data is located in the file: {file_name}. '
                    'First, read the file to understand the structure. '
                    'Then write a complete python script to perform the analysis and print the result. '
                    'Do not use markdown blocks in the output, just the raw python code.',
        expected_output='A valid python script.',
        agent=coder
    )

    execution_task = Task(
        description='Execute the python script provided by the previous task. '
                    'Return the output of the execution.',
        expected_output='The result of the analysis.',
        agent=executor
    )

    # 3. Create the Crew
    crew = Crew(
        agents=[coder, executor],
        tasks=[coding_task, execution_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew.kickoff()

if __name__ == "__main__":
    # Example usage
    print("## Starting Crew in tools.py ##")
    file_name = input('send me the file name: ')
    # Using persons.csv as requested
    result = run_crew(file_name, 'calculate the avg age of the persons in the file')
    print("\n\n########################")
    print("## Result ##")
    print("########################\n")
    print(result)

