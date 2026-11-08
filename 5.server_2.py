from mcp.server.fastmcp import FastMCP
from datetime import date
from pathlib import Path

mcp = FastMCP("Personal Assistant")

# Create sandbox directory if it doesn't exist
SANDBOX_DIR = Path(__file__).parent / "sandbox"
SANDBOX_DIR.mkdir(exist_ok=True)


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
    task_file = SANDBOX_DIR / "tasks.txt"

    with open(task_file, "a", encoding="utf-8") as file:
        file.write(task + "\n")

    return f"Task added: {task}" 

@mcp.resource("tasks://all")
def get_all_tasks() -> str:
    """Get all saved tasks."""

    task_file = SANDBOX_DIR / "tasks.txt"

    if not task_file.exists():
        return "No tasks found."

    return task_file.read_text(encoding="utf-8") 

@mcp.prompt()
def travel_planner(destination: str, days: int) -> str:
    """Generate a travel planning prompt."""

    return f"""
    Create a travel itinerary for {destination}
    covering {days} days.

    Include:
    - Tourist attractions
    - Local food
    - Transportation
    - Estimated expenses
    """


if __name__ == "__main__":
    mcp.run(transport="stdio")