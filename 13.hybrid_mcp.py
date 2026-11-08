
import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp, MCPServerStdio
from dotenv import load_dotenv 

load_dotenv() 


async def main():

    # Local Filesystem MCP server
    files_params = {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "./sandbox"
        ]
    }

    async with (
        # Remote Context7 server
        MCPServerStreamableHttp(
            name="Context7",
            params={
                "url": "https://mcp.context7.com/mcp"
            }
        ) as context7,

        # Remote Humaps server
        MCPServerStreamableHttp(
            name="Humaps",
            params={
                "url": "https://api.humaps.org/mcp"
            }
        ) as humaps,

        # Local Filesystem server
        MCPServerStdio(
            name="Filesystem",
            params=files_params,
            client_session_timeout_seconds=60
        ) as files_server
    ):

        # Create Agent
        agent = Agent(
            name="Research Assistant",
            instructions="""
            You are a research assistant.

            - Use Context7 for software documentation.
            - Use Humaps for public datasets and geographic research.
            - Use Filesystem to save research reports as Markdown files.
            - Always save the final report inside the sandbox directory.
            """,
            model="gpt-4o-mini",
            mcp_servers=[
                context7,
                humaps,
                files_server
            ]
        )

        # Research query
        result = await Runner.run(
            agent,
            """
            Find public datasets about population in Japan.

            Explain:
            1. Available datasets and their sources.
            2. What information they contain.
            3. How to analyze them using Python.
            4. Possible visualizations.

            Create a well-organized Markdown report and save it
            as japan-population-research.md.
            """
        )

        print("\nAgent Response:")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())

'''Multi-server MCP Research Assistant that connects to two remote MCP servers, 
Context7 for documentation and Humaps for public datasets and geographic research, 
alongside a local Filesystem MCP server using STDIO'''