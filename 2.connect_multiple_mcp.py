import asyncio
from agents.mcp import MCPServerStdio


async def main():

    # Fetch server
    fetch_params = {
        "command": "uvx",
        "args": ["--with", "mcp<2", "mcp-server-fetch"]
    }

    # Filesystem server
    files_params = {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "./sandbox"
        ]
    }

    async with MCPServerStdio(
        params=fetch_params,
        client_session_timeout_seconds=60
    ) as fetch_server:

        async with MCPServerStdio(
            params=files_params,
            client_session_timeout_seconds=60
        ) as files_server:

            # Discover Fetch tools
            fetch_tools = await fetch_server.list_tools()

            # Discover Filesystem tools
            files_tools = await files_server.list_tools()

            print("\nFETCH TOOLS")
            for tool in fetch_tools:
                print(tool.name)

            print("\nFILESYSTEM TOOLS")
            for tool in files_tools:
                print(tool.name)


if __name__ == "__main__":
    asyncio.run(main())