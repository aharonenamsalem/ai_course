from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# initialize the server
mcp = FastMCP("Products Service")
# api base
base_url = "https://fakestoreapi.com/products"


# define the methods
@mcp.tool()
async def get_products() :
    """Returns products data from an external api

    """
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url)
        return response.json()



if __name__ == "__main__":
    print("Starting name origin server...")
    mcp.run(transport='stdio')