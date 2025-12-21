import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({
  name: "Users Service",
  version: "1.0.0",
});



import { z } from "zod";

server.tool(
  "getUser",
  { id: z.number() },
  async ({ id }) => {
   
    //Your code goes here..
    
    return {
      content: [
        {
          type: "text",
          text: // The data to return,
        },
      ],
    };
  },
);

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const transport = new StdioServerTransport();
await server.connect(transport);