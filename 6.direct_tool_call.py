
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_path = Path(__file__).parent / "5.server.py"

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP connection
            await session.initialize()

            # Discover tools
            tools = await session.list_tools()

            print("Available tools:")
            for tool in tools.tools:
                print("-", tool.name)

            # Call tool 1
            result1 = await session.call_tool(
                "calculate_age",
                arguments={"birth_year": 2001}
            )

            print("\nAge:", result1.content)

            # Call tool 2
            result2 = await session.call_tool(
                "get_current_date",
                arguments={}
            )

            print("\nDate:", result2.content)

            # Call tool 3
            result3 = await session.call_tool(
                "add_task",
                arguments={"task": "Learn MCP tool execution"}
            )

            print("\nTask:", result3.content)


if __name__ == "__main__":
    asyncio.run(main())
