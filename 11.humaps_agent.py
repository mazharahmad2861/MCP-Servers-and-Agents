
import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from dotenv import load_dotenv 

load_dotenv()


async def main():

    async with MCPServerStreamableHttp(
        name="Humaps",
        params={
            "url": "https://api.humaps.org/mcp"
        }
    ) as server:

        tools = await server.list_tools()

        print("Humaps Tools:")
        for tool in tools:
            print("-", tool.name)

        agent = Agent(
            name="Public Data Researcher",
            instructions="Research public datasets using Humaps tools. Explain sources and limitations.",
            model="gpt-4o-mini",
            mcp_servers=[server]
        )

        result = await Runner.run(
            agent,
            "Find authoritative public data sources about "
            "population and healthcare access in Japan. "
            "Summarize the available data."
        )

        print("\nAgent Response:")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
