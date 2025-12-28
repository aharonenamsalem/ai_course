from mcp.server.fastmcp import FastMCP
import json
mcp = FastMCP("http-request")


@mcp.tool()
def http_request(url: str) -> str:
    """Make an HTTP GET request to the specified URL and return the response content as a string."""
    import requests

    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text

mcp.run(transport="stdio")
# STDIO
# HTTP-STREAMABLE
# SSE