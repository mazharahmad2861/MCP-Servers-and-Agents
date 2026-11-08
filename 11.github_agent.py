
import asyncio
import os
from dotenv import load_dotenv

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

load_dotenv()


async def main():

    token = os.getenv("GITHUB_TOKEN")

    async with MCPServerStreamableHttp(
        name="GitHub",
        params={
            "url": "https://api.githubcopilot.com/mcp/readonly",
            "headers": {
                "Authorization": f"Bearer {token}"
            }
        }
    ) as server:

        tools = await server.list_tools()

        print("GitHub Tools:")
        for tool in tools:
            print("-", tool.name)

        agent = Agent(
            name="GitHub Assistant",
            instructions="You are a GitHub research assistant. Use GitHub tools to answer questions.",
            model="gpt-4o-mini",
            mcp_servers=[server]
        )

        result = await Runner.run(
            agent,
            "Find information about the repository "
            "modelcontextprotocol/servers. "
            "Summarize its purpose and main features."
        )

        print("\nAgent Response:")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
