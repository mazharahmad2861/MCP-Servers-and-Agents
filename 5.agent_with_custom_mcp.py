import asyncio
import sys
import os
import subprocess
import functools

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
import agents.mcp.server
from dotenv import load_dotenv 

load_dotenv()  # Load environment variables from .env file


# Windows STDIO workaround
if os.name == "nt":
    agents.mcp.server.stdio_client = functools.partial(
        agents.mcp.server.stdio_client,
        errlog=subprocess.DEVNULL
    )


async def main():

    async with MCPServerStdio(
        params={
            "command": sys.executable,
            "args": ["5.server_2.py"]
        },
        client_session_timeout_seconds=60
    ) as server:

        # Discover tools
        tools = await server.list_tools()

        print("\nAvailable tools:")
        for tool in tools:
            print("-", tool.name)

        # Create Agent
        agent = Agent(
            name="Personal Assistant",
            instructions="You are a helpful personal assistant. Use available tools whenever required.",
            model="gpt-4o-mini",
            mcp_servers=[server]
        )

        # Multiple queries
        result1 = await Runner.run(
            agent,
            "Calculate my age if I was born in 2001."
        )

        result2 = await Runner.run(
            agent,
            "What is today's date?"
        )

        result3 = await Runner.run(
            agent,
            "Add 'Complete Python assignment' to my task list."
        )

        result4 = await Runner.run(
            agent,
            "Add 'Buy groceries' to my task list."
        )

        # Print results
        print("\n========== RESULTS ==========")

        print("\nResult 1:", result1.final_output)
        print("\nResult 2:", result2.final_output)
        print("\nResult 3:", result3.final_output)
        print("\nResult 4:", result4.final_output)


if __name__ == "__main__":
    asyncio.run(main())