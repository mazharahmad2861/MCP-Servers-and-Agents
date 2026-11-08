from mcp.server.fastmcp import FastMCP
from datetime import date

mcp = FastMCP("Personal Assistant")


@mcp.tool()
def get_current_date() -> str:
    """Get today's date."""
    return str(date.today())


@mcp.tool()
def calculate_age(birth_year: int) -> int:
    """Calculate age using birth year."""
    return date.today().year - birth_year


@mcp.tool()
def add_task(task: str) -> str:
    """Add a task to the to-do list."""
    with open("tasks.txt", "a") as file:
        file.write(task + "\n")

    return f"Task added: {task}" 




if __name__ == "__main__":
    mcp.run(transport="streamable-http")