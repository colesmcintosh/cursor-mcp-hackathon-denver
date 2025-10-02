# FastMCP Python Server Development Guide

You are developing a FastMCP server in Python using the `fastmcp` package (version 2.0+).

## Quick Start

```python
from fastmcp import FastMCP

mcp = FastMCP(name="MyServer")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()  # Default: stdio transport
    # For HTTP: mcp.run(transport="http", port=8000)
```

---

## Core Components

### 1. Tools (`@mcp.tool`)
Tools are executable functions that LLMs can call. Use type annotations for automatic validation.

**Basic Tool:**
```python
@mcp.tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
```

**Advanced Tool with Metadata:**
```python
from typing import Annotated, Literal
from pydantic import Field

@mcp.tool(
    name="search_products",
    description="Search the product catalog",
    tags={"catalog", "search"},
    annotations={
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def search_products(
    query: Annotated[str, Field(description="Search query")],
    category: Literal["electronics", "books", "clothing"] | None = None,
    max_results: Annotated[int, Field(ge=1, le=100)] = 10
) -> list[dict]:
    """Search products with optional category filtering."""
    # Implementation...
    return [{"id": 1, "name": "Product"}]
```

**With Context (logging, progress, etc):**
```python
from fastmcp import Context

@mcp.tool
async def process_file(filepath: str, ctx: Context) -> dict:
    """Process a file with progress reporting."""
    await ctx.info(f"Starting to process {filepath}")
    await ctx.report_progress(0, 100)
    
    # Do work...
    await ctx.report_progress(50, 100)
    
    await ctx.info("Processing complete")
    await ctx.report_progress(100, 100)
    return {"status": "done", "filepath": filepath}
```

**Supported Return Types:**
- `str` → TextContent
- `dict`, Pydantic models → JSON (structured output with schema)
- `bytes` → Base64 blob
- `list[...]` → Multiple content blocks
- `ToolResult` → Full control over content and structured output

**Type Annotations:**
- Basic: `int`, `float`, `str`, `bool`
- Collections: `list[T]`, `dict[K,V]`, `set[T]`, `tuple[...]`
- Optional: `str | None`, `Optional[str]`
- Constrained: `Literal["a", "b"]`, `Enum`
- Complex: Pydantic models, `datetime`, `date`, `Path`, `UUID`

**Excluding Parameters from Schema:**
```python
@mcp.tool(exclude_args=["api_key"])
def call_api(endpoint: str, api_key: str = "default") -> dict:
    """Call API - api_key hidden from LLM but available to function"""
    # api_key won't appear in tool schema but can be set by server
    ...
```

### 2. Resources (`@mcp.resource`)
Resources provide read-only access to data. Can be static or dynamic (templates).

**Static Resource:**
```python
@mcp.resource("data://config")
def get_config() -> dict:
    """Application configuration."""
    return {"theme": "dark", "version": "1.0"}
```

**Resource Template (with parameters):**
```python
@mcp.resource("weather://{city}/current")
async def get_weather(city: str) -> dict:
    """Get current weather for a city."""
    # Fetch from weather API
    return {"city": city, "temp": 72, "condition": "sunny"}
```

**Wildcard Parameters (RFC 6570):**
```python
@mcp.resource("files://{filepath*}")
def get_file_content(filepath: str) -> str:
    """Get content from any file path."""
    return Path(filepath).read_text()
```

**Query Parameters:**
```python
@mcp.resource("data://{id}{?format,limit}")
def get_data(id: str, format: str = "json", limit: int = 100) -> str:
    """Get data with optional format and limit."""
    # Query params must have defaults
    return f"Data {id} as {format} (limit: {limit})"
```

**Multiple URI Templates for Same Function:**
```python
def lookup_user(name: str | None = None, email: str | None = None) -> dict:
    """Look up user by name or email"""
    if email:
        return find_by_email(email)
    return find_by_name(name)

# Register multiple ways to access
mcp.resource("users://by-name/{name}")(lookup_user)
mcp.resource("users://by-email/{email}")(lookup_user)
```

**Static File Resources:**
```python
from fastmcp.resources import FileResource
from pathlib import Path

readme = FileResource(
    uri="file://README.md",
    path=Path("./README.md"),
    name="Project README",
    description="Main project documentation",
    mime_type="text/markdown"
)
mcp.add_resource(readme)
```

### 3. Prompts (`@mcp.prompt`)
Reusable message templates for LLMs.

```python
from fastmcp.prompts import Message

@mcp.prompt
def analyze_data(data_uri: str, analysis_type: str = "summary") -> str:
    """Generate a data analysis prompt."""
    return f"Please perform a '{analysis_type}' analysis on data at {data_uri}."

@mcp.prompt
def roleplay(character: str, situation: str) -> list[Message]:
    """Multi-message conversation starter."""
    return [
        Message(f"You are {character}. Situation: {situation}"),
        Message("I understand. What happens next?", role="assistant")
    ]
```

**Complex Types in Prompts (Auto-converted from JSON strings):**
```python
@mcp.prompt
def analyze_metrics(
    numbers: list[int],
    metadata: dict[str, str],
    threshold: float
) -> str:
    """Analyze numerical data with metadata."""
    avg = sum(numbers) / len(numbers)
    return f"Analyzing {len(numbers)} values (avg: {avg}, threshold: {threshold})"
```

---

## MCP Context

Access MCP features (logging, progress, sampling) by adding `ctx: Context` parameter:

```python
from fastmcp import Context

@mcp.tool
async def process_data(data_uri: str, ctx: Context) -> dict:
    """Process data with progress reporting."""
    await ctx.info(f"Processing {data_uri}")
    
    # Read a resource
    resource = await ctx.read_resource(data_uri)
    
    # Report progress
    await ctx.report_progress(50, 100)
    
    # Ask LLM for help
    summary = await ctx.sample(f"Summarize: {resource}")
    
    await ctx.report_progress(100, 100)
    return {"summary": summary.text}
```

**Context Features:**
- Logging: `ctx.debug()`, `ctx.info()`, `ctx.warning()`, `ctx.error()`
- Progress: `ctx.report_progress(progress, total)`
- Resources: `ctx.read_resource(uri)`
- LLM Sampling: `ctx.sample(prompt)` - Ask the client's LLM to generate text
- Request Info: `ctx.request_id`, `ctx.client_id`
- User Input: `ctx.request_user_input(prompt, schema)` - Request structured input from user

**Example: User Elicitation**
```python
@mcp.tool
async def create_user(ctx: Context) -> dict:
    """Create a user by requesting information."""
    user_data = await ctx.request_user_input(
        "Enter user details",
        schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "email"]
        }
    )
    return {"created": user_data}
```

---

## Server Configuration

```python
mcp = FastMCP(
    name="MyServer",
    instructions="Server description for clients",
    auth=None,  # Add authentication if needed
    include_tags={"public"},  # Only expose these tags
    exclude_tags={"internal"},  # Hide these tags
    on_duplicate_tools="error",  # "error"|"warn"|"replace"|"ignore"
    on_duplicate_resources="warn",
    on_duplicate_prompts="replace",
    mask_error_details=False,  # Hide sensitive error info
    include_fastmcp_meta=True,  # Include FastMCP metadata in responses
)
```

### Tag-Based Filtering

```python
# Define components with tags
@mcp.tool(tags={"public", "utility"})
def public_tool() -> str:
    return "Available to all"

@mcp.tool(tags={"internal", "admin"})
def admin_tool() -> str:
    return "Admin only"

# Filter at server level
public_server = FastMCP(include_tags={"public"})
admin_server = FastMCP(include_tags={"admin"}, exclude_tags={"deprecated"})
```

### Dynamic Enable/Disable

```python
@mcp.tool
def feature_tool() -> str:
    return "Feature result"

# Control availability at runtime
if feature_enabled:
    feature_tool.enable()
else:
    feature_tool.disable()

# Check status
if feature_tool.enabled:
    print("Feature is available")
```

---

## Error Handling

```python
from fastmcp.exceptions import ToolError, ResourceError

@mcp.tool
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        # Always sent to client regardless of mask_error_details
        raise ToolError("Division by zero not allowed")
    return a / b

@mcp.resource("data://{id}")
def get_data(id: str) -> dict:
    """Get data by ID with error handling."""
    if id not in database:
        raise ResourceError(f"Data {id} not found")
    return database[id]
```

**Error Masking for Security:**
```python
mcp = FastMCP(name="SecureServer", mask_error_details=True)

@mcp.tool
def secure_operation(key: str) -> dict:
    """Operation with masked errors."""
    try:
        # If this fails, clients see generic error (due to mask_error_details)
        result = sensitive_api_call(key)
        return result
    except Exception as e:
        # Log the real error for debugging
        print(f"Error: {e}")
        # But raise user-friendly error
        raise ToolError("Operation failed. Please check your input.")
```

---

## Running the Server

**Local (stdio):**
```python
if __name__ == "__main__":
    mcp.run()
```

**HTTP:**
```python
if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

**FastMCP CLI:**
```bash
fastmcp run server.py:mcp --transport http --port 8000
```

**With Custom Routes (Health Checks, etc):**
```python
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

@mcp.custom_route("/metrics", methods=["GET"])
async def metrics(request: Request) -> JSONResponse:
    return JSONResponse({"tools": len(mcp._tools), "uptime": get_uptime()})

if __name__ == "__main__":
    mcp.run(transport="http")
```

---

## Advanced Patterns

### 1. Server Composition (Mounting)

```python
# Create sub-servers
weather = FastMCP(name="Weather")
@weather.tool
def get_forecast() -> dict:
    return {"temp": 72}

calendar = FastMCP(name="Calendar")
@calendar.tool
def get_events() -> list:
    return [{"title": "Meeting"}]

# Combine into main server
main = FastMCP(name="MainServer")
main.mount(weather, prefix="weather")
main.mount(calendar, prefix="cal")

# Now have tools: weather.get_forecast, cal.get_events
```

### 2. Lifespan Management (Startup/Shutdown)

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # Startup
    print("Initializing database connection...")
    db = await connect_to_database()
    app.state.db = db
    
    yield
    
    # Shutdown
    print("Closing database connection...")
    await db.close()

mcp = FastMCP(name="MyServer", lifespan=lifespan)

@mcp.tool
async def query_db(sql: str) -> list:
    """Query database using connection from lifespan."""
    db = mcp.state.db
    return await db.execute(sql)
```

### 3. Middleware

```python
from fastmcp.server.middleware import Middleware
from mcp.types import Request, Result

class LoggingMiddleware(Middleware):
    async def process_request(self, request: Request) -> Request:
        print(f"Incoming: {request.method}")
        return request
    
    async def process_response(self, response: Result) -> Result:
        print(f"Outgoing: {response}")
        return response

mcp = FastMCP(name="MyServer")
mcp.add_middleware(LoggingMiddleware())
```

### 4. Dependency Injection

```python
from typing import Annotated

class Database:
    def query(self, sql: str) -> list:
        return []

def get_db() -> Database:
    return Database()

@mcp.tool
async def fetch_users(
    limit: int,
    db: Annotated[Database, Depends(get_db)]
) -> list:
    """Fetch users with injected database."""
    return db.query(f"SELECT * FROM users LIMIT {limit}")
```

### 5. Proxy Servers

```python
from fastmcp import Client

# Create proxy to existing MCP server
backend = Client("http://example.com/mcp")
proxy = FastMCP.as_proxy(backend, name="ProxyServer")

# Now use proxy like any FastMCP server
await proxy.run()
```

### 6. OpenAPI Integration

```python
import httpx
from fastmcp import FastMCP

# Generate server from OpenAPI spec
spec = httpx.get("https://api.example.com/openapi.json").json()
mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=httpx.AsyncClient(),
    name="APIServer"
)

# Or from FastAPI app
from fastapi import FastAPI
app = FastAPI()
mcp = FastMCP.from_fastapi(app=app)
```

---

## Testing Your Server

### Unit Testing Tools

```python
# test_server.py
import pytest
from server import mcp

@pytest.mark.asyncio
async def test_calculate_sum():
    """Test the calculate_sum tool."""
    result = await mcp.call_tool("calculate_sum", {"a": 5, "b": 3})
    assert result == 8

@pytest.mark.asyncio
async def test_tool_validation():
    """Test that invalid input is rejected."""
    with pytest.raises(ValueError):
        await mcp.call_tool("calculate_sum", {"a": "not a number", "b": 3})

@pytest.mark.asyncio
async def test_resource():
    """Test resource access."""
    result = await mcp.read_resource("data://config")
    assert result["theme"] == "dark"
```

### Integration Testing

```python
from fastmcp import Client

@pytest.mark.asyncio
async def test_full_integration():
    """Test server via client connection."""
    # Start server in background
    server = await start_server()
    
    async with Client("http://localhost:8000/mcp") as client:
        # List tools
        tools = await client.list_tools()
        assert len(tools) > 0
        
        # Call tool
        result = await client.call_tool("greet", {"name": "World"})
        assert "Hello, World" in result
    
    await server.stop()
```

### Manual Testing with FastMCP CLI

```bash
# Test tool call directly
fastmcp dev server.py:mcp --test-tool greet '{"name": "World"}'

# Start interactive shell
fastmcp dev server.py:mcp --interactive

# Run with verbose logging
fastmcp run server.py:mcp --log-level DEBUG
```

---

## Debugging Tips

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

mcp = FastMCP(name="MyServer")
```

Or via environment variable:
```bash
export FASTMCP_LOG_LEVEL=DEBUG
python server.py
```

### Inspect Tool Schemas

```python
# See what schema LLM receives
for tool in mcp.list_tools():
    print(f"{tool.name}: {tool.inputSchema}")
```

### Test Without Cursor

```python
# server.py
if __name__ == "__main__":
    import sys
    if "--test" in sys.args:
        # Run test calls
        result = mcp.call_tool_sync("my_tool", {"param": "test"})
        print(result)
    else:
        mcp.run()
```

### Common Issues

**Tool not being called by LLM:**
- Make description more specific about when to use it
- Add examples in the description
- Check parameter names are intuitive

**"Unknown tool" errors:**
- Verify tool is enabled: `tool.enabled`
- Check tag filters aren't excluding it
- Confirm server reloaded in Cursor

**Type validation errors:**
- Use `Field` to add constraints and better descriptions
- Check type annotations are correct
- Test with invalid data to see error messages

---

## Performance Optimization

### Async for I/O Operations

```python
import asyncio
import httpx

@mcp.tool
async def fetch_multiple_urls(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs concurrently."""
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

### Caching Expensive Operations

```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def expensive_computation(input: str) -> str:
    """Cached expensive operation."""
    time.sleep(2)  # Simulate expensive work
    return input.upper()

@mcp.tool
def process(input: str) -> str:
    """Tool using cached function."""
    return expensive_computation(input)
```

### Lazy Loading Resources

```python
@mcp.resource("data://large-dataset")
def get_large_dataset() -> dict:
    """Only loaded when requested, not on server startup."""
    return load_data_from_disk()  # Heavy operation
```

---

## Best Practices

1. **Type Everything**: Use type annotations for all parameters and returns
2. **Document Clearly**: Write descriptive docstrings and field descriptions
3. **Use Async**: Prefer `async def` for I/O operations (API calls, DB queries)
4. **Validate Input**: Use Pydantic `Field` for constraints (ge, le, pattern, etc.)
5. **Handle Errors**: Raise clear exceptions; use `ToolError`/`ResourceError` for client feedback
6. **Tag Components**: Use tags for organization and filtering
7. **Stateless Design**: Keep servers stateless for easy restarts
8. **Structured Output**: Use Pydantic models or dicts for complex return types
9. **Test Thoroughly**: Write tests for all tools and error cases
10. **Log Important Events**: Use context logging for debugging

### Code Organization

```
my-mcp-server/
├── server.py           # Main server definition
├── tools/              # Tool implementations
│   ├── __init__.py
│   ├── weather.py
│   └── calendar.py
├── resources/          # Resource handlers
│   ├── __init__.py
│   └── data.py
├── models.py           # Pydantic models
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── tests/              # Test files
│   ├── test_tools.py
│   └── test_resources.py
└── README.md           # Documentation
```

---

## Installation

```bash
# Using uv (recommended)
uv add fastmcp

# Using pip
pip install fastmcp

# With optional dependencies
pip install fastmcp[dev]  # Development tools
pip install fastmcp[httpx]  # HTTP client support
pip install fastmcp[testing]  # Testing utilities

# Verify
fastmcp version
```

---

## Dependencies

Always pin exact versions in production:
```txt
fastmcp==2.12.3
httpx>=0.27.0  # If making HTTP requests
pydantic>=2.0.0  # For advanced validation
aiofiles>=23.0.0  # For async file operations
```

---

## Deployment

### FastMCP Cloud (free for personal)
1. Push to GitHub
2. Sign in at https://fastmcp.cloud
3. Create project with entrypoint `server.py:mcp`
4. Get URL like `https://your-project.fastmcp.app/mcp`

### Self-Hosted with Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "server.py"]
```

### Railway/Heroku/Fly.io

Create `Procfile`:
```
web: python server.py
```

Or use FastMCP CLI:
```
web: fastmcp run server.py:mcp --transport http --port $PORT
```

---

## Example Full Server

```python
from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
from typing import Annotated, Literal
import asyncio

mcp = FastMCP(name="ExampleServer")

class User(BaseModel):
    username: str
    email: str
    age: int | None = None

@mcp.tool
async def create_user(user: User, ctx: Context) -> dict:
    """Create a new user with logging."""
    await ctx.info(f"Creating user {user.username}")
    # Simulate database operation
    await asyncio.sleep(0.1)
    return {"id": "123", "username": user.username, "email": user.email}

@mcp.tool(tags={"query"})
async def search_users(
    query: Annotated[str, Field(min_length=1)],
    limit: Annotated[int, Field(ge=1, le=100)] = 10,
    status: Literal["active", "inactive", "all"] = "all"
) -> list[dict]:
    """Search users with validation and filtering."""
    # Simulate database query
    await asyncio.sleep(0.1)
    return [
        {"id": "1", "username": "alice", "status": "active"},
        {"id": "2", "username": "bob", "status": "inactive"}
    ][:limit]

@mcp.resource("users://{user_id}")
async def get_user(user_id: str) -> dict:
    """Get user by ID as a resource."""
    return {"id": user_id, "username": f"user_{user_id}", "status": "active"}

@mcp.resource("users://{user_id}/posts{?limit}")
async def get_user_posts(user_id: str, limit: int = 10) -> list[dict]:
    """Get user's posts with optional limit."""
    return [
        {"id": i, "title": f"Post {i}", "author": user_id}
        for i in range(limit)
    ]

@mcp.prompt
def ask_about_user(user_id: str, aspect: str = "general") -> str:
    """Generate a prompt to analyze a user."""
    return f"Analyze the {aspect} information about user at users://{user_id}"

if __name__ == "__main__":
    mcp.run()
```

---

## Quick Reference Card

### Tool Patterns
```python
# Basic
@mcp.tool
def tool(param: str) -> dict: ...

# With validation
@mcp.tool
def tool(param: Annotated[str, Field(min_length=1)]) -> dict: ...

# Async with context
@mcp.tool
async def tool(param: str, ctx: Context) -> dict:
    await ctx.info("Starting")
    ...

# With error handling
@mcp.tool
def tool(param: str) -> dict:
    if not param:
        raise ToolError("Param required")
    ...
```

### Resource Patterns
```python
# Static
@mcp.resource("data://item")
def get_item() -> dict: ...

# Template
@mcp.resource("data://{id}")
def get_by_id(id: str) -> dict: ...

# With query params
@mcp.resource("data://{id}{?format}")
def get_with_format(id: str, format: str = "json") -> str: ...

# Wildcard
@mcp.resource("files://{path*}")
def get_file(path: str) -> str: ...
```

### Common Types
```python
# Simple
str, int, float, bool

# Optional
str | None, Optional[str]

# Collections
list[str], dict[str, int], set[int]

# Constrained
Literal["a", "b"], Annotated[int, Field(ge=0, le=100)]

# Complex
datetime, date, Path, UUID, Pydantic models
```

---

Now implement your server following these patterns! 🚀
