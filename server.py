"""FastMCP server providing hackathon resources."""

from pathlib import Path
from fastmcp import FastMCP

APP_NAME = "denver-hackathon"
APP_DESCRIPTION = "Provides the MCP Server Hackathon overview and information."

app = FastMCP(name=APP_NAME, instructions=APP_DESCRIPTION)

BASE_DIR = Path(__file__).parent
HACKATHON_MARKDOWN_PATH = BASE_DIR / "resources" / "hackathon_overview.md"

HACKATHON_MARKDOWN = HACKATHON_MARKDOWN_PATH.read_text(encoding="utf-8")

@app.tool()
def get_hackathon_info() -> str:
    """Get the complete hackathon overview with all information about the MCP Server Hackathon.
    
    Returns:
        The full hackathon overview document including format, getting started guide, 
        project ideas, resources, and quick reference.
    """
    return HACKATHON_MARKDOWN


if __name__ == "__main__":
    app.run()
