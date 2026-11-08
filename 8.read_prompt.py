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

            # Discover prompts
            prompts = await session.list_prompts()

            print("Available prompts:")
            for prompt in prompts.prompts:
                print("-", prompt.name)

            # Get a specific prompt
            result = await session.get_prompt(
                "travel_planner",
                arguments={
                    "destination": "Japan",
                    "days": "5"
                }
            )

            print("\nGenerated Prompt:")
            for message in result.messages:
                print(message.content.text)


if __name__ == "__main__":
    asyncio.run(main())