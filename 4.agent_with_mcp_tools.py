import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

from dotenv import load_dotenv
load_dotenv()  


async def main():

    fetch_params = {
        "command": "uvx",
        "args": ["--with", "mcp<2", "mcp-server-fetch"]
    }

    files_params = {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "./sandbox"
        ]
    }

    async with (
        MCPServerStdio(params=fetch_params) as fetch_server,
        MCPServerStdio(params=files_params) as files_server
    ):

        agent = Agent(
            name="Research Assistant",
            instructions="Use available tools to complete the user's task.",
            model="gpt-4o-mini",
            mcp_servers=[fetch_server, files_server]
        )

        

        result = await Runner.run(
                    agent,
                    "Plan a 5-day trip to Spain with a daily itinerary, best cities, activities to do, cusines to try, adventures, a complete itineary. Save everything in spain-trip.md."
                )

        print(result.final_output)
        


if __name__ == "__main__":
    asyncio.run(main())