You are developing a new FastMCP server in Python. Use the fastmcp package to:

1. Register any MCP tools your workflow needs.
2. Expose relevant resources using `@app.resource` with helpful markdown.
3. Provide prompts that give Cursor users clear next steps for interacting with your server.

Expectations:
- Validate and parse JSON arguments with Pydantic models or dataclasses.
- Return structured results that Cursor can render cleanly.
- Keep the server stateless when possible so it restarts reliably.
- Add inline comments where the implementation could benefit from quick context.

Start by outlining the server’s responsibilities, then implement each tool and resource. Include lightweight tests or manual verification steps where practical so the server is demo-ready.
