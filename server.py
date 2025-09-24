"""FastMCP server providing hackathon resources and starter prompts."""

from fastmcp import FastMCP
from fastmcp.prompts import Message
from mcp.types import PromptMessage

APP_NAME = "fastmcp-hackathon"
APP_DESCRIPTION = (
    "Provides the hackathon overview markdown and a starter prompt for building "
    "FastMCP servers with Python."
)

app = FastMCP(name=APP_NAME, instructions=APP_DESCRIPTION)

HACKATHON_MARKDOWN = """## Overview

This hackathon is about building **MCP (Model Context Protocol) servers** that work inside **Cursor**. You can build in **any language or framework**. Python with **FastMCP** is a recommended setup because it is quick to prototype and easy to demo inside Cursor.

---

## Goals

- Learn how MCP plugs into Cursor
- Build and demo your own MCP server
- Explore unique ideas that go beyond existing connectors

---

## Architecture at a Glance

```mermaid
flowchart TD
  A[Cursor] --> B[LLM in Cursor]
  B --> C{MCP Client Layer}
  C -->|List tools| D[MCP Server]
  C -->|Call tool with args| D
  D --> E{Tool Handler}
  E -->|Local action| F[Filesystem or Local DB]
  E -->|External call| G[Third Party API]
  F --> H[Structured Result]
  G --> H[Structured Result]
  H --> I{MCP Response}
  I --> J[Cursor Renders Output]
  J --> K[User Iterates in Editor]

```

---

## Getting Started

### Fast path in Python with FastMCP

```bash
git clone <https://github.com/modelcontextprotocol/fastmcp-starter>
cd fastmcp-starter
pip install -r requirements.txt
python server.py

```

Add to `.cursor/config.json`:

```json
{
  "mcpServers": {
    "fastmcp-demo": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}

```

Restart Cursor to load the server.

### Use any language

- Implement MCP request and response contracts
- Expose tools that accept JSON args
- Print stdout and read stdin as required by MCP

---

## Unique Project Ideas

Skip the obvious GitHub, Slack, Notion, and Gmail clones.

- **Mood Board MCP**
Input a vibe such as “cozy autumn coding”. Return a small set of curated Unsplash or Pexels links.
- **Weather plus Vibes MCP**
Get local forecast and pair it with a matching focus playlist link.
- **Regex Builder MCP**
Convert plain English rules into a working regex with sample test cases.
- **Snippet Swap MCP**
Query a local JSON or SQLite store to fetch code snippets by topic. No API keys needed.
- **Persona Generator MCP**
Produce quick UX persona objects from a one line description.
- **Commit Poem MCP**
Turn a git commit message into a short haiku or limerick.
- **Emoji Mapper MCP**
Annotate any paragraph with contextually fitting emojis.
- **Denver Coffee Crawl MCP**
Return top five indie coffee shops for a given neighborhood.

---

## Rules and Format

- Use any language or framework
- Python with FastMCP is recommended for speed
- Solo or teams of up to three
- Judging criteria
    - **Utility**
    - **Creativity**
    - **Execution inside Cursor**

---

## Resources

- Cursor Docs: https://cursor.sh/docs
- MCP Example Servers: https://github.com/modelcontextprotocol
- Python FastMCP Repo: https://github.com/modelcontextprotocol/python-sdk

---

## Let’s Build

Keep the scope tight. Make it work in Cursor. Demo proudly.
"""

PROMPT_TEMPLATE = """You are developing a new FastMCP server in Python. Use the fastmcp package to:

1. Register any MCP tools your workflow needs.
2. Expose relevant resources using `@app.resource` with helpful markdown.
3. Provide prompts that give Cursor users clear next steps for interacting with your server.

Expectations:
- Validate and parse JSON arguments with Pydantic models or dataclasses.
- Return structured results that Cursor can render cleanly.
- Keep the server stateless when possible so it restarts reliably.
- Add inline comments where the implementation could benefit from quick context.

Start by outlining the server’s responsibilities, then implement each tool and resource. Include lightweight tests or manual verification steps where practical so the server is demo-ready.
"""

@app.resource(
    "resource://hackathon-overview",
    name="Hackathon Overview",
    description="Markdown overview for the MCP hackathon",
    mime_type="text/markdown",
)
def hackathon_overview() -> str:
    """Return the hackathon overview resource."""
    return HACKATHON_MARKDOWN


@app.prompt(
    "fastmcp-python-starter",
    description="Prompt template for building FastMCP servers with Python",
)
def fastmcp_python_prompt() -> list[PromptMessage]:
    """Provide a ready-to-use prompt for FastMCP Python development."""
    return [
        Message(
            role="assistant",
            content=(
                "You are an expert FastMCP engineer helping a developer build a "
                "Python MCP server that integrates cleanly with Cursor."
            ),
        ),
        Message(role="user", content=PROMPT_TEMPLATE),
    ]


if __name__ == "__main__":
    app.run()
