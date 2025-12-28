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
    args=["C:\\Users\\miche\\Desktop\\AI5 -PUBLIC\\Demos\\Agents\\CrewAI\\Demo3_Agent_MCP\\mcp_server\\math_mcp_server.py"],
    
), 
    
    StdioServerParameters(
    command="python",
    args=["C:\\Users\\miche\\Desktop\\AI KIVUN\\4 - MCP\\Demo2_Python\\main.py"]
),      
    ]




with MCPServerAdapter(servers_params) as tools:
    for tool in tools:
        print(tool.name)     
             
    agent = Agent(
        role="Mathematician",
        goal="Perform math operations",
        backstory="An expert in math",
        tools=tools,
        verbose=True
    )
    
    task = Task(
        description="Solve the math problem given to you: {math_problem}",
        expected_output="The correct answer to the math problem using your available tools.",
        agent=agent
    )
    
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    
    result = crew.kickoff(inputs={"math_problem": "What is (4 * 2) ** 2? after you get the result, give me the origin of the name 'Avi' and present the results in bullets"})
    print("Final result: ", result)