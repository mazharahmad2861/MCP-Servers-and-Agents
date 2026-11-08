import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():

    async with streamable_http_client(
        "http://127.0.0.1:8000/mcp"
    ) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")
            for tool in tools.tools:
                print("-", tool.name)

            result = await session.call_tool(
                "calculate_age",
                arguments={"birth_year": 2001}
            )

            print("\nAge:", result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())