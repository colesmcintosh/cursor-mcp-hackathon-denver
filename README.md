# MCP Demo

A FastMCP reference server that ships with a hackathon overview resource and a reusable starter prompt. Clone the repo, install the dependencies (or build the Docker image), and you have an MCP server that Cursor can load immediately.

## Requirements
- Python 3.12+
- `pip` (ships with Python)
- Docker 24+ (optional, for containerised usage)

## Local Setup
1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Run the FastMCP server (it listens on STDIN/STDOUT as required by the MCP spec):
   ```bash
   python server.py
   ```

## Docker Setup
1. Build the image:
   ```bash
   docker build -t mcp-demo .
   ```
2. Run the container, keeping STDIN open so MCP clients can communicate with it:
   ```bash
   docker run --rm -i mcp-demo
   ```
   Add `-t` if you want an interactive TTY while debugging, for example `docker run --rm -it mcp-demo`.

## Cursor Configuration
Add the MCP server to `.cursor/config.json` using either a local Python interpreter or the Docker image.

**Local Python:**
```json
{
  "mcpServers": {
    "fastmcp-demo": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/absolute/path/to/mcp-demo"
    }
  }
}
```

**Docker container:**
```json
{
  "mcpServers": {
    "fastmcp-demo": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--volume",
        "/absolute/path/to/mcp-demo:/app",
        "mcp-demo"
      ]
    }
  }
}
```
Mounting the repository lets you iterate on `server.py` without rebuilding the image. Omit the `--volume` flag if you prefer a read-only container.

Restart Cursor after updating the configuration so it can spawn the server.

## Tests
Run the test suite to ensure everything is wired correctly:
```bash
pytest
```

## Project Structure
- `server.py` – FastMCP server exposing the hackathon overview resource and starter prompt
- `tests/` – Pytest suite that validates resources and prompt wiring
- `Dockerfile` / `.dockerignore` – Container build assets for running the server in Docker

Happy hacking!
