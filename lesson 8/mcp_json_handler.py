from mcp.server.fastmcp import FastMCP
import json
mcp = FastMCP("json-handler")

filename = "data.json"
@mcp.tool()
def parse_json(json_string: str) -> dict:
    """Parse a JSON string and return the corresponding dictionary."""
    return json.loads(json_string)  
@mcp.tool()
def append_json_to_file(data: dict) -> str:  
    """Append a dictionary as a JSON object to a file, ensuring the file content remains a valid JSON array and no duplicate IDs exist."""
    try:
        # Read the existing content of the file
        with open(filename, "r") as f:
            content = f.read().strip()
            if content:
                existing_data = json.loads(content)
                if not isinstance(existing_data, list):
                    raise ValueError("File content is not a JSON array.")
            else:
                existing_data = []
    except FileNotFoundError:
        existing_data = []
    except json.JSONDecodeError:
        raise ValueError("File content is not valid JSON.")

    # Check for duplicate IDs
    if "id" in data:
        for item in existing_data:
            if item.get("id") == data["id"]:
                raise ValueError(f"Duplicate ID {data['id']} found in the file.")

    # Append the new data to the existing list
    existing_data.append(data)

    # Write the updated list back to the file
    with open(filename, "w") as f:
        json.dump(existing_data, f, indent=4)

    return filename

mcp.run(transport="stdio")
# STDIO
# HTTP-STREAMABLE
# SSE