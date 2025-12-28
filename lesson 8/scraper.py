from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

import os 
from dotenv import load_dotenv
load_dotenv()
# os.environ["OPENAI_API_KEY"] = "..."

servers_params = [
    StdioServerParameters(
    command="python",
    args=["mcp_http_request.py"],
    
), 
    
    StdioServerParameters(
    command="python",
    args=["mcp_json_handler.py"]
),      
    ]




with MCPServerAdapter(servers_params) as tools:
    for tool in tools:
        print(tool.name)     
             
    http_master = Agent(
        role="Http_handler",
        goal="""
            receives a website {url}, makes an http request to get the data from the website,
        and process the data to answer the question
        """,
        backstory="you are a web browser and http request handler",
        tools=tools,
        verbose=True
    )
    json_handler = Agent(
        role="Json_handler",
        goal="""
            receives test data from the HTTP handler, processes it, and extracts the required information
            to answer the question.
        """,
        backstory="you are a JSON processor and data extractor",
        tools=tools,
        context_agent=http_master,
        verbose=True
    )
    
    http_task = Task(
        description="make an HTTP request to the given {url} and retrieve the data",
        expected_output="the raw data from the HTTP request",
        agent=http_master
    )
    
    json_task = Task(
        description="process the raw data from the HTTP request and extract the required information and write the data to json file",
        expected_output="file path",
        agent=json_handler
    )
    
    crew = Crew(
        agents=[http_master, json_handler],
        tasks=[http_task, json_task],
        verbose=True
    )
    
    result = crew.kickoff(inputs={"url": "https://dummyjson.com/products/3"})
    print("Final result: ", result)