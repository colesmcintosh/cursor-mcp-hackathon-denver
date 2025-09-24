"""FastMCP server providing hackathon resources and starter prompts."""

from pathlib import Path

from fastmcp import FastMCP
from fastmcp.prompts import Message
from mcp.types import PromptMessage

APP_NAME = "fastmcp-hackathon"
APP_DESCRIPTION = (
    "Provides the hackathon overview markdown and a starter prompt for building "
    "FastMCP servers with Python."
)

app = FastMCP(name=APP_NAME, instructions=APP_DESCRIPTION)

BASE_DIR = Path(__file__).parent
HACKATHON_MARKDOWN_PATH = BASE_DIR / "resources" / "hackathon_overview.md"
PROMPT_TEMPLATE_PATH = BASE_DIR / "prompts" / "fastmcp_python_starter.md"

HACKATHON_MARKDOWN = HACKATHON_MARKDOWN_PATH.read_text(encoding="utf-8")
PROMPT_TEMPLATE = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")

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
