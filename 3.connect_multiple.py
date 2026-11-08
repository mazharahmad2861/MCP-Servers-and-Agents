import asyncio
import os
import functools
import subprocess
import agents.mcp.server

from agents.mcp import MCPServerStdio


# Windows STDIO workaround
if os.name == "nt":
    agents.mcp.server.stdio_client = functools.partial(
        agents.mcp.server.stdio_client,
        errlog=subprocess.DEVNULL
    )


async def main():

    # Fetch MCP server
    fetch_params = {
        "command": "uvx",
        "args": [
            "--with", "mcp<2",
            "mcp-server-fetch"
        ]
    }

    # Filesystem MCP server
    sandbox_path = os.path.abspath("sandbox")
    os.makedirs(sandbox_path, exist_ok=True)

    files_params = {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            sandbox_path
        ]
    }

    async with (
        MCPServerStdio(
            params=fetch_params,
            client_session_timeout_seconds=120
        ) as fetch_server,

        MCPServerStdio(
            params=files_params,
            client_session_timeout_seconds=120
        ) as files_server
    ):

        # Discover tools
        fetch_tools = await fetch_server.list_tools()
        files_tools = await files_server.list_tools()

        print("\nFETCH TOOLS")
        print("Total:", len(fetch_tools))

        for tool in fetch_tools:
            print(tool.name)

        print("\nFILESYSTEM TOOLS")
        print("Total:", len(files_tools))

        for tool in files_tools:
            print(tool.name)


if __name__ == "__main__":
    asyncio.run(main())