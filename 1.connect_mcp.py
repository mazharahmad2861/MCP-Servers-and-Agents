import asyncio
from agents.mcp import MCPServerStdio


async def main():

    # Configure MCP server
    params = {
        "command": "uvx",
        "args": [
            "--with", "mcp<2",
            "mcp-server-fetch"
        ]
    }

    # Connect to MCP server
    async with MCPServerStdio(
        params=params,
        client_session_timeout_seconds=60
    ) as server:

        # Discover available tools
        tools = await server.list_tools()

        for tool in tools:
            print("Tool Name:", tool.name)
            print("Description:", tool.description)
            print("Input Schema:", tool.input_schema)


if __name__ == "__main__":
    asyncio.run(main())