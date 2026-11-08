import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

from dotenv import load_dotenv
load_dotenv()


async def main():

    async with MCPServerStreamableHttp(
        name="Context7",
        params={
            "url": "https://mcp.context7.com/mcp"
        }
    ) as server:

        tools = await server.list_tools()

        print("Available tools:")
        for tool in tools:
            print("-", tool.name)

        agent = Agent(
            name="Documentation Assistant",
            instructions="""
            You are a documentation research assistant.
            Use Context7 tools to find relevant documentation.
            """,
            model="gpt-4o-mini",
            mcp_servers=[server]
        )

        result = await Runner.run(
            agent,
            "Find the latest LangGraph documentation and explain how state and nodes work."
        )

        print("\nAgent response:")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())