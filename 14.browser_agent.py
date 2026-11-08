
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStdio


load_dotenv()

# Create sandbox directory
BASE_DIR = Path(__file__).parent
SANDBOX_DIR = BASE_DIR / "sandbox"
SANDBOX_DIR.mkdir(exist_ok=True)


async def main():

    # Playwright MCP Server
    playwright_params = {
        "command": "npx",
        "args": [
            "-y",
            "@playwright/mcp@latest",
            "--browser",
            "chromium"
        ]
    }

    # Filesystem MCP Server
    filesystem_params = {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            str(SANDBOX_DIR)
        ]
    }

    async with (

        MCPServerStdio(
            name="Playwright Browser",
            params=playwright_params,
            client_session_timeout_seconds=60
        ) as browser_server,

        MCPServerStdio(
            name="Filesystem",
            params=filesystem_params,
            client_session_timeout_seconds=60
        ) as filesystem_server

    ):

        # Discover Playwright tools
        browser_tools = await browser_server.list_tools()

        print("\nPlaywright Tools:")
        for tool in browser_tools:
            print("-", tool.name)

        # Discover Filesystem tools
        filesystem_tools = await filesystem_server.list_tools()

        print("\nFilesystem Tools:")
        for tool in filesystem_tools:
            print("-", tool.name)

        # Create Browser Agent
        agent = Agent(
            name="Browser Research Assistant",

            instructions="""
            You are an intelligent browser research assistant.

            BROWSER INSTRUCTIONS:
            - Use Playwright MCP to browse websites.
            - Navigate to relevant websites.
            - Search for information and inspect webpage content.
            - Visit multiple relevant sources when necessary.
            - Do not invent information or claim to have visited
              pages you have not actually inspected.

            RESEARCH INSTRUCTIONS:
            - Organize findings into meaningful sections.
            - Prefer reliable and authoritative sources.
            - Include source URLs in your report.
            - Avoid unnecessary or irrelevant information.

            FILESYSTEM INSTRUCTIONS:
            - Use Filesystem MCP to save the final report.
            - Save all reports inside the sandbox directory.
            - Use Markdown format and save in .md files in the sandbox directory.
            

            Do not perform purchases, submit forms, or make
            irreversible changes to websites.
            """,

            model="gpt-4o-mini",

            mcp_servers=[
                browser_server,
                filesystem_server
            ]
        )

        # User query
        query = """
        Research the top 10 tourist attractions in Kinnaur district Himachal Pradesh, India.

        Include:
        1. Location and introduction.
        2. Main attractions and activities.
        3. Best time to visit.
        4. Estimated visiting expenses where reliable information
           is available.
        5. Travel recommendations.
        6. Source URLs.

        Create a well-organized Markdown report.

        Save it as kinnaur-tourism-guide.md.
        """

        result = await Runner.run(
            agent,
            query,
            max_turns=20
        )

        print("\n========== FINAL RESPONSE ==========")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
