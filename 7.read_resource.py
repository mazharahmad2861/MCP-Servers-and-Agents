import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_path = Path(__file__).parent / "5.server_2.py"

    params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)]
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            # Discover resources
            resources = await session.list_resources()

            for resource in resources.resources:
                print("Resource:", resource.uri)

            # Read resource
            result = await session.read_resource("tasks://all")

            for content in result.contents:
                print("\nSaved Tasks:")
                print(content.text)


if __name__ == "__main__":
    asyncio.run(main())