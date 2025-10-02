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

@app.tool()
def get_hackathon_info(query: str) -> str:
    """Get the hackathon overview.
    
    Args:
        query: The search term or topic to find in the hackathon overview
        
    Returns:
        The hackathon overview
    """
    return HACKATHON_MARKDOWN

@app.tool()
def expert_fastmcp_builder(query: str) -> str:
    """Get the prompt template.
    
    Args:
        query: The search term or topic to find in the prompt template
    """
    return PROMPT_TEMPLATE


if __name__ == "__main__":
    app.run()
