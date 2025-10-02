# MCP Demo

A FastMCP reference server that ships with a hackathon overview resource and a reusable starter prompt. Clone the repo, install the dependencies (or build the Docker image), and you have an MCP server that Cursor can load immediately.

## Requirements
- Python 3.12+
- `pip` (ships with Python)
- Docker 24+ (optional, for containerised usage)

## Deployment Options

This server can run in two modes:
1. **Local STDIO** (for Cursor integration) - see setup below
2. **Remote HTTP/SSE** (for public access, ChatGPT, etc.) - see [DEPLOY.md](DEPLOY.md)

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
1. Build the image (the Dockerfile installs into an isolated virtual environment and runs as a non-root user):
   ```bash
   docker build -t mcp-demo:latest .
   ```
2. Run the container, keeping STDIN open so MCP clients can communicate with it:
   ```bash
   docker run --rm -i mcp-demo:latest
   ```
   Add `-t` if you want an interactive TTY while debugging.
3. Mount your working directory if you want to live-edit the code without rebuilding:
   ```bash
   docker run --rm -it -v "$(pwd)":/app mcp-demo:latest
   ```
   The container's default command is `python server.py`, so it behaves exactly like the local workflow.

## Deploying the Container
The image is ready to drop into any container platform (AWS ECS/Fargate, AWS App Runner, Railway, Fly.io, etc.). A typical deployment looks like:

1. Tag the image for your registry and push it:
   ```bash
   docker tag mcp-demo:latest ghcr.io/<your-user>/mcp-demo:latest
   docker push ghcr.io/<your-user>/mcp-demo:latest
   ```
   Replace the registry URL with ECR, Docker Hub, or your preferred destination.
2. Create a service that runs the container with the default command `python server.py`. MCP servers communicate over STDIN/STDOUT, so no ports need to be exposed unless you run a proxy alongside it.
3. (Optional) If your platform expects an HTTP interface, pair the container with an MCP bridge/relay that converts HTTP/WebSocket traffic to the STDIO protocol.

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
