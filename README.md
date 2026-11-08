# Model Context Protocol (MCP) 

## 1. What is MCP?

**Model Context Protocol (MCP)** is an open standard that enables AI applications to connect with external tools, data sources and services through a standardized communication protocol.

### Problem MCP Solves
- Eliminates the need for separate, custom integrations for every AI application.
- Provides a standardized way to connect AI models with external systems.
- Makes integrations reusable across different MCP-compatible applications.
- Allows AI agents to interact with databases, APIs, filesystems, browsers and other services.

**Important:** MCP is a communication protocol, not an AI model or an agent framework.

---

## 2. MCP Architecture

MCP has three primary components:

### MCP Host
The application in which the AI assistant or agent operates.

Examples: Claude Desktop or an application built using OpenAI Agents SDK.

### MCP Client
The component responsible for establishing and managing communication with MCP servers.

Responsibilities:
- Establishes connections.
- Initializes sessions.
- Discovers available tools, resources and prompts.
- Sends requests and receives responses.

### MCP Server
An application that exposes capabilities such as tools, resources and prompts to MCP clients.

Examples: Filesystem, GitHub, PostgreSQL and Playwright servers.

**Remember:** Host manages the AI application, Client handles communication, and Server exposes capabilities.

---

## 3. Core MCP Capabilities

MCP servers can expose three important capabilities.

### A. Tools

Tools are executable functions that allow an AI application to perform operations.

Examples:
- Searching the web.
- Creating or modifying files.
- Executing database queries.
- Sending emails.
- Interacting with APIs.

Tools are generally invoked by the AI application when the model decides that an operation is required.

### B. Resources

Resources expose data or context to an AI application.

Examples:
- Files.
- Database records.
- Application information.
- Configuration data.

Resources are identified using URIs and are primarily intended for providing information rather than executing actions.

### C. Prompts

Prompts are reusable prompt templates exposed by an MCP server.

Examples:
- Daily planner.
- Code review instructions.
- Research templates.

They help applications reuse predefined instructions for common tasks.

### Tools vs Resources vs Prompts

| Feature | Purpose |
|---|---|
| Tools | Execute operations |
| Resources | Provide information |
| Prompts | Provide reusable instructions |

---

## 4. MCP Communication Protocol

MCP uses **JSON-RPC 2.0** for structured communication between clients and servers.

It defines how requests, responses and notifications are exchanged.

Important MCP methods:

| Method | Purpose |
|---|---|
| `initialize` | Initialize the connection |
| `tools/list` | Discover available tools |
| `tools/call` | Execute a tool |
| `resources/list` | Discover resources |
| `resources/read` | Read a resource |
| `prompts/list` | Discover prompts |
| `prompts/get` | Retrieve a prompt |

---

## 5. MCP Transports

Transport determines how messages travel between MCP clients and servers.

### A. STDIO

- Used primarily for local MCP servers.
- The client launches the server as a subprocess.
- Communication happens through standard input and standard output.
- Commonly used for local Python and Node.js MCP servers.

Examples: Filesystem and local custom MCP servers.

### B. Streamable HTTP

- Used for communication with HTTP-based MCP servers.
- The server can run independently of the client.
- Supports streaming responses.
- Suitable for remote MCP integrations.

### C. HTTP + SSE

SSE stands for Server-Sent Events.

- Used by earlier MCP implementations for server-to-client streaming.
- It is a legacy transport approach.
- Streamable HTTP is the recommended modern HTTP transport.

### STDIO vs Streamable HTTP

| STDIO | Streamable HTTP |
|---|---|
| Local process communication | HTTP communication |
| Client launches server | Server runs independently |
| Uses stdin/stdout | Uses HTTP |
| Common for local integrations | Common for remote integrations |

---

## 6. How an AI Agent Uses MCP Tools

An agent does not directly execute an MCP server's code. The agent framework manages the interaction.

Typical execution process:

1. The user submits a request.
2. The agent receives available tool descriptions and input schemas.
3. The LLM determines which tool is appropriate.
4. The LLM generates a tool call with the required arguments.
5. The MCP client sends the request to the corresponding server.
6. The MCP server executes the requested operation.
7. The result is returned to the agent.
8. The LLM uses the result to generate the final response.

### Responsibilities

| Component | Responsibility |
|---|---|
| LLM | Decides which tool to call |
| Agent framework | Manages agent execution |
| MCP Client | Communicates with the server |
| MCP Server | Executes the requested operation |
| External system | Provides or processes the underlying data |

**Important:** MCP does not decide which tool the LLM should call. It provides the standardized mechanism for discovering and executing tools.

---

## 7. Building Custom MCP Servers

The Python MCP SDK provides functionality for creating custom MCP servers.

**FastMCP** simplifies server development through Python decorators.

Important concepts:

- `FastMCP`: Creates an MCP server.
- `@mcp.tool()`: Registers a function as an MCP tool.
- `@mcp.resource()`: Registers a resource.
- `@mcp.prompt()`: Registers a reusable prompt.
- `mcp.run()`: Starts the server using the selected transport.

### Tool Parameters and Arguments

A tool's function signature defines its input parameters.

Python type annotations help generate the tool's input schema.

Common data types include:
- `str`
- `int`
- `float`
- `bool`
- `list`
- `dict`

**Parameter vs Argument:**
- Parameter: Variable defined in a function signature.
- Argument: Actual value passed when calling the function.

A tool's input schema describes the accepted arguments, their types and required fields.

### Synchronous vs Asynchronous Tools

MCP tools can be synchronous or asynchronous.

Asynchronous functions are useful when operations involve network requests, file operations or other I/O-bound tasks.

---

## 8. MCP Client

An MCP client connects to an MCP server and interacts with its exposed capabilities.

Important client operations:

| Operation | Purpose |
|---|---|
| Initialize | Establish an MCP session |
| List tools | Discover available tools |
| Call tool | Execute a tool |
| List resources | Discover available resources |
| Read resource | Retrieve resource contents |
| List prompts | Discover available prompts |
| Get prompt | Retrieve a prompt template |

**Important:** MCP can be used without an LLM. A Python application can directly connect to an MCP server, discover tools and execute them.

---

## 9. MCP with OpenAI Agents SDK

We used the OpenAI Agents SDK as our agent framework.

Important components:

- `Agent`: Defines the agent, its instructions and available capabilities.
- `Runner.run()`: Executes the agent.
- `MCPServerStdio`: Connects to local STDIO MCP servers.
- `MCPServerStreamableHttp`: Connects to Streamable HTTP MCP servers.
- `mcp_servers`: Registers MCP servers with an agent.
- `max_turns`: Limits the number of agent execution turns.

### Important Concepts

**Agent instructions:** Define the agent's role, behaviour and tool usage guidelines.

**Tool discovery:** The agent framework obtains available tool definitions from connected MCP servers.

**Multiple MCP servers:** An agent can connect to several MCP servers simultaneously and access their tools.

**max_turns:** It limits agent execution cycles, not the exact number of tool calls.

---

## 10. Connecting Multiple MCP Servers

An agent can use multiple MCP servers to perform complex tasks.

For example:

| MCP Server | Responsibility |
|---|---|
| Context7 | Retrieve library documentation |
| Humaps | Access geographic information |
| Filesystem | Read and write files |
| Playwright | Browser automation |
| GitHub | Repository operations |

Each server exposes its own capabilities. The agent can select tools from different servers depending on the user's request.

This makes it possible to build agents that combine browsing, research, coding, databases and file operations.

---

## 11. Remote MCP Servers We Explored

### Context7
Provides access to up-to-date library documentation.

Useful for coding agents that need current API references and framework documentation.

### Humaps
Provides geographic and spatial information through MCP tools.

Useful for applications involving location and geographic data.

### GitHub
Provides repository-related capabilities depending on the server implementation and permissions.

Useful for code analysis, repository exploration and development workflows.

Remote servers generally use Streamable HTTP, while local servers commonly use STDIO.

---

## 12. Important MCP Servers

| Server | Primary purpose |
|---|---|
| Filesystem | File and directory operations |
| Playwright | Browser automation |
| GitHub | Repository interaction |
| Context7 | Library documentation |
| Fetch | Retrieving webpage content |
| SQLite | Local database operations |
| PostgreSQL | Relational database operations |
| Memory | Persistent information storage |
| Slack | Communication and messaging |
| Google Drive | Document access |
| Docker | Container management |
| AWS | Cloud resource interaction |

MCP is extensible. Developers can create custom servers for their own APIs, databases and internal applications.

---

## 13. Playwright MCP

Playwright MCP enables AI agents to interact with web browsers through MCP tools.

Typical capabilities:
- Navigate to websites.
- Click buttons and links.
- Fill forms.
- Inspect webpage content.
- Interact with browser elements.
- Capture screenshots.

### Playwright vs Fetch

| Playwright | Fetch |
|---|---|
| Browser automation | Web content retrieval |
| Supports interaction with webpages | Primarily retrieves webpage content |
| Useful for dynamic websites | Useful for straightforward content extraction |
| Can click and fill forms | Does not provide general browser interaction |

---

## 14. Filesystem MCP

Filesystem MCP allows agents to interact with files and directories.

Typical capabilities:
- Read files.
- Write files.
- List directories.
- Search files.
- Create directories.
- Perform supported file operations.

### Important Concept: Restricted Access

Filesystem servers can be restricted to specific directories.

This follows the principle of least privilege: an agent should only receive access to the files and directories it actually needs.

---

## 15. Browser Research Agent

We combined Playwright MCP and Filesystem MCP to build a browser research agent.

### Responsibilities

**Playwright MCP:**
- Browses websites.
- Extracts relevant information.
- Inspects multiple sources.

**Filesystem MCP:**
- Creates and manages files.
- Saves generated research reports.

**AI Agent:**
- Understands the research request.
- Decides which browser tools to call.
- Organizes collected information.
- Produces the final report.

### Important Learning: Deterministic Operations

We encountered a situation where the agent generated a report in the terminal but did not save it using Filesystem MCP.

We addressed this by explicitly writing the agent's final output to a Markdown file using Python.

This demonstrates an important production principle:

**Do not rely entirely on LLM instructions for critical application operations. Use deterministic application logic to guarantee important outcomes.**

---

## 16. Python Concepts Used in MCP

### Async and Await
MCP applications commonly use asynchronous programming for communication and I/O operations.

- `async def`: Defines an asynchronous function.
- `await`: Waits for an asynchronous operation.
- `asyncio.run()`: Runs an asynchronous program.

### Context Managers
`async with` manages the lifecycle of asynchronous connections.

When the block exits, the connection is closed.

### Pathlib
Python's `pathlib` library helps manage file and directory paths across operating systems.

### Environment Variables
Environment variables are used to provide configuration and secrets without hardcoding sensitive values.

### Subprocesses
Local STDIO MCP servers commonly run as separate processes launched by the MCP client.

---

## 17. MCP Security and Best Practices

Important considerations when developing production MCP applications:

1. **Authentication:** Verify the identity of clients accessing remote servers.
2. **Authorization:** Restrict operations according to user permissions.
3. **Least Privilege:** Give servers only the permissions they require.
4. **Input Validation:** Validate tool arguments before execution.
5. **Filesystem Restrictions:** Restrict file access to permitted directories.
6. **Human Approval:** Require confirmation for sensitive or irreversible operations.
7. **Error Handling:** Handle tool failures and connection problems.
8. **Timeouts:** Prevent operations from waiting indefinitely.
9. **Logging:** Record tool calls and failures for debugging and auditing.
10. **Untrusted Content:** Treat external webpage content and tool outputs as data, not trusted instructions.

---

## 18. Important Interview Takeaways

- MCP is a protocol, not an agent framework.
- Host, Client and Server have different responsibilities.
- Tools execute operations, Resources expose data and Prompts provide reusable instructions.
- MCP uses JSON-RPC 2.0 for structured communication.
- STDIO is commonly used for local servers.
- Streamable HTTP is used for HTTP-based communication.
- An LLM selects tools; the MCP client handles communication.
- MCP can be used without an LLM.
- FastMCP simplifies custom Python MCP server development.
- Multiple MCP servers can be connected to one agent.
- Tool schemas describe the inputs expected by tools.
- Security and permissions are essential when exposing external capabilities.

---

## 19. Final Quick Revision

| Term | Meaning |
|---|---|
| MCP | Model Context Protocol |
| Host | AI application |
| Client | Communicates with MCP servers |
| Server | Exposes capabilities |
| Tool | Executable operation |
| Resource | Data or context |
| Prompt | Reusable instruction template |
| JSON-RPC | Communication message format |
| STDIO | Local process transport |
| Streamable HTTP | HTTP-based transport |
| FastMCP | Python MCP server framework |
| `@mcp.tool()` | Registers a tool |
| `@mcp.resource()` | Registers a resource |
| `@mcp.prompt()` | Registers a prompt |
| `list_tools()` | Discovers tools |
| `call_tool()` | Executes a tool |
| MCP ClientSession | Manages an MCP client session |
| OpenAI Agents SDK | Agent framework used in our practice |
| Playwright MCP | Browser automation |
| Filesystem MCP | File operations |
| Context7 | Documentation retrieval |
| `max_turns` | Maximum agent execution turns |

---
## Important Code Concepts

### 1. FastMCP – Creating an MCP Server

```python
mcp = FastMCP("My Server")

@mcp.tool()
@mcp.resource("tasks://all")
@mcp.prompt()

mcp.run(transport="stdio")
```

- `FastMCP()` – Creates an MCP server.
- `@mcp.tool()` – Registers a tool.
- `@mcp.resource()` – Registers a resource.
- `@mcp.prompt()` – Registers a reusable prompt.
- `mcp.run()` – Starts the server.

### 2. MCPServerStdio – Local Server Connection

```python
params = {
    "command": "npx",
    "args": ["-y", "package-name"]
}

MCPServerStdio(
    name="My Server",
    params=params
)
```

- `command` – Executable used to launch the server (`python`, `npx`).
- `args` – Arguments passed to the executable.
- `params` – Local server process configuration.
- `name` – Server identifier.

**Useful:** `sys.executable` launches the server using the current Python environment.

### 3. MCPServerStreamableHttp – Remote Server Connection

```python
MCPServerStreamableHttp(
    name="Remote Server",
    params={
        "url": "https://example.com/mcp",
        "headers": {"Authorization": "Bearer TOKEN"}
    }
)
```

- `url` – Remote MCP endpoint.
- `headers` – HTTP headers, commonly used for authentication.
- Used to connect to HTTP-based MCP servers.

### 4. Connection Management

```python
async with MCPServerStdio(...) as server:
    ...
```

- `async with` – Manages connection lifecycle and closes the connection when the block exits.
- Multiple servers can be connected using multiple context managers.

```python
mcp_servers=[server1, server2]
```

Registers multiple MCP servers with an agent.

### 5. Agent – OpenAI Agents SDK

```python
agent = Agent(
    name="Assistant",
    instructions="Use available tools.",
    model="gpt-4o-mini",
    mcp_servers=[server]
)
```

- `Agent()` – Creates an AI agent.
- `instructions` – Defines agent behaviour.
- `model` – Specifies the LLM.
- `mcp_servers` – Connects MCP servers to the agent.

### 6. Runner.run() and max_turns

```python
result = await Runner.run(
    agent,
    "Research a topic",
    max_turns=20
)

result.final_output
```

- `Runner.run()` – Executes the agent.
- `max_turns` – Maximum agent execution turns, not tool calls.
- `final_output` – Contains the final agent response.

### 7. Direct MCP Client Operations

```python
await session.initialize()

tools = await session.list_tools()

result = await session.call_tool(
    "add",
    arguments={"a": 10, "b": 20}
)
```

Important methods:

| Method | Purpose |
|---|---|
| `initialize()` | Initialize session |
| `list_tools()` | Discover tools |
| `call_tool()` | Execute a tool |
| `list_resources()` | Discover resources |
| `read_resource()` | Read a resource |
| `list_prompts()` | Discover prompts |
| `get_prompt()` | Retrieve a prompt |

**Remember:** MCP tools can be called directly without an LLM.

### 8. Important Python Concepts

```python
async def main():
    result = await session.list_tools()

asyncio.run(main())
```

- `async` – Defines an asynchronous function.
- `await` – Waits for an asynchronous operation.
- `asyncio.run()` – Runs the asynchronous program.

```python
from pathlib import Path

BASE_DIR = Path(__file__).parent
SANDBOX_DIR = BASE_DIR / "sandbox"
SANDBOX_DIR.mkdir(exist_ok=True)
```

- `Path(__file__).parent` – Gets the current script's directory.
- `mkdir(exist_ok=True)` – Creates a directory if it doesn't exist.

```python
report_path.write_text(report, encoding="utf-8")
```

Writes the report to a file.

### 9. Important Parameter Distinctions

| Parameter | Meaning |
|---|---|
| `command` | Executable to launch a local server |
| `args` | Command-line arguments |
| `env` | Server environment variables |
| `cwd` | Server working directory |
| `url` | Remote MCP endpoint |
| `headers` | HTTP request headers |
| `params` | Server connection/process configuration |
| `arguments` | Actual values passed to a tool |
| `max_turns` | Maximum agent execution turns |

**Key distinction:** `MCPServerStdio` uses local process configuration (`command`, `args`), whereas `MCPServerStreamableHttp` uses HTTP configuration (`url`, `headers`).

**Core takeaway:** MCP provides a standardized way for AI applications to discover and use external capabilities. Understanding its architecture, communication, transports, server development, tool execution and integration with agent frameworks is the foundation for building practical Agentic AI applications.
