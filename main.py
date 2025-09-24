"""CLI entry point for running the FastMCP hackathon server."""

from server import app


def main() -> None:
    """Run the FastMCP server using the shared application instance."""
    app.run()


if __name__ == "__main__":
    main()
