<div align="center">
  <img src="assets/cursor-denver.png" alt="Cursor Denver" width="400"/>
  
  # MCP Demo
  
  [![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
  [![FastMCP](https://img.shields.io/badge/FastMCP-powered-purple.svg)](https://github.com/jlowin/fastmcp)
  [![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  
  **A production-ready FastMCP reference server with hackathon resources and reusable starter prompts**
  
</div>

---

## Overview

A FastMCP server with comprehensive hackathon overview resources and reusable starter prompts. Clone, install dependencies or build the Docker image, and you have an MCP server that Cursor can load immediately.

## Requirements

| Component | Version | Required |
|-----------|---------|----------|
| Python | 3.12+ | Yes |
| uv | Latest | Yes |
| Docker | 24+ | Optional |
| Node.js | 18+ | Optional |

---

## Quick Start

### Local Python Setup

```bash
# Install dependencies and run
uv sync
uv run server.py
```

### Docker Setup

```bash
# Build the image
docker build -t mcp-demo:latest .

# Run the container
docker run --rm -i mcp-demo:latest

# Development mode with live reload
docker run --rm -it -v "$(pwd)":/app mcp-demo:latest
```

### Remote MCP (no local setup)

```bash
npx -y mcp-remote https://cursor-denver-mcp-hackathon.fastmcp.app/mcp
```

---

## Deployment Options

| Mode | Use Case | Setup | Best For |
|------|----------|-------|----------|
| Local STDIO | Cursor integration | Simple | Development |
| Remote HTTP/SSE | Public access | Advanced | Production |
| Docker Local | Isolated environment | Medium | Testing |
| Docker Remote | Cloud deployment | Advanced | Production |

### Container Registry Push

```bash
# GitHub Container Registry
docker tag mcp-demo:latest ghcr.io/<your-user>/mcp-demo:latest
docker push ghcr.io/<your-user>/mcp-demo:latest

# Docker Hub
docker tag mcp-demo:latest <your-user>/mcp-demo:latest
docker push <your-user>/mcp-demo:latest
```

---

## Cursor Configuration

Add to `~/.cursor/mcp.json`:

<table>
<tr>
<th>Local (uv)</th>
<th>Docker Container</th>
</tr>
<tr>
<td>

```json
{
  "mcpServers": {
    "fastmcp-demo": {
      "command": "uv",
      "args": ["run", "server.py"],
      "cwd": "/absolute/path/to/mcp-demo"
    }
  }
}
```

</td>
<td>

```json
{
  "mcpServers": {
    "fastmcp-demo": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--volume",
        "/absolute/path/to/mcp-demo:/app",
        "mcp-demo"
      ]
    }
  }
}
```

</td>
</tr>
</table>

### Remote MCP Server

```json
{
  "mcpServers": {
    "denver-hackathon": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://cursor-denver-mcp-hackathon.fastmcp.app/mcp"
      ]
    }
  }
}
```

Restart Cursor after updating configuration.

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_server.py -v
```

---

## Project Structure

```
mcp-demo/
├── server.py                 # FastMCP server
├── main.py                   # Alternative entry point
├── Dockerfile                # Container build
├── requirements.txt          # Dependencies
├── pyproject.toml            # Project config
├── resources/
│   └── hackathon_overview.md
├── prompts/
│   └── fastmcp_python_starter.md
└── tests/
    ├── conftest.py
    └── test_server.py
```

---

## License

MIT License

---

<div align="center">
  
Built for the Cursor Denver Hackathon

</div>
