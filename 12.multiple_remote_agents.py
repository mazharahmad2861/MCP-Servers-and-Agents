
import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from dotenv import load_dotenv 

load_dotenv()


async def main():

    async with (
        MCPServerStreamableHttp(
            name="Context7",
            params={
                "url": "https://mcp.context7.com/mcp"
            }
        ) as context7,

        MCPServerStreamableHttp(
            name="Humaps",
            params={
                "url": "https://api.humaps.org/mcp"
            }
        ) as humaps
    ):

        agent = Agent(
            name="Research Assistant",
            instructions="""
            You are a research assistant.

            Use Context7 for software documentation.
            Use Humaps for public datasets and geographic research.
            Select the appropriate tools based on the user's request.
            """,
            model="gpt-4o-mini",
            mcp_servers=[context7, humaps]
        )

        result = await Runner.run(
            agent,
            "Find public datasets about population in Japan "
            "and explain how I could use Python to analyze them."
        )

        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
