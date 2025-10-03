## Overview

Welcome to the MCP Server Hackathon! Build **MCP (Model Context Protocol) servers** that extend Cursor's capabilities using **any language or framework**.

**What is MCP?** A protocol that allows AI assistants to safely access external data and tools. It's a standardized way for LLMs to call functions, read data, and interact with services beyond their training data.

**What You'll Build:** Custom tools that integrate seamlessly into Cursor, solving real problems right inside your IDE.

---

## Hackathon Format

**Team Size:** Solo or teams of up to 3 people

**Language:** Use any programming language or framework you're comfortable with. Popular choices include Python, TypeScript/Node.js, Go, or Rust.

**Deliverables:**
- Working MCP server that runs in Cursor
- Live demo showing 2-3 real use cases

---

### The Flow

1. **User interacts in Cursor**: You write a message in Cursor's chat
2. **Cursor discovers tools**: Cursor connects to your MCP server and lists available tools
3. **LLM decides to use a tool**: Based on your request, Claude decides which tool to call
4. **Tool execution**: Your server receives the request, validates parameters, and executes the tool
5. **Results returned**: Your tool returns structured data back to Cursor
6. **Cursor displays results**: The LLM uses the results to craft a response to you

---

## Getting Started

### Choose Your Tech Stack

**Python (FastMCP)** - Quick prototyping, great for demos
```bash
git clone https://github.com/modelcontextprotocol/fastmcp-starter
pip install fastmcp && python server.py
```

**TypeScript/Node.js** - Official MCP SDK, strong typing
```bash
npm install @modelcontextprotocol/sdk
```

**Go, Rust, or others** - Implement the MCP protocol directly using JSON-RPC 2.0

### Configure Cursor

Add to `.cursor/mcp.json`:

**Python:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

**Node.js:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/absolute/path/to/build/index.js"]
    }
  }
}
```

**Important:** Use absolute paths and restart Cursor completely after changes.

### Verify It Works

1. Open Cursor's command palette (Cmd/Ctrl+Shift+P)
2. Search for "MCP" to see if your server is loaded
3. Try chatting with Cursor and mention your tool by name

---

## Implementation Essentials

Your MCP server needs to:

- **Communicate via stdio or HTTP**: Read/write JSON-RPC 2.0 messages
- **Implement core methods**: `initialize`, `tools/list`, `tools/call`
- **Define tool schemas**: Clear descriptions and input validation
- **Return structured data**: JSON responses the LLM can understand

See the [MCP Specification](https://spec.modelcontextprotocol.io) for complete protocol details.

---

## Tool Design Best Practices

**Keep Tools Focused**  
Each tool should do one thing well. Create separate tools like `get_weather(city)` instead of one `do_everything(action, data)` tool.

**Return Structured Data**  
Return JSON objects, not formatted strings:
```json
{
  "id": "123",
  "name": "John",
  "age": 30,
  "active": true
}
```

**Write Clear Descriptions**  
Tool descriptions help the LLM decide when to use your tool. Be specific about what it does.

**Validate Inputs**  
Use your language's validation tools to validate parameters. Reject invalid input early with clear error messages.

---

## Project Ideas

**The best projects solve real problems you've experienced.** Build something unique!

### Think Beyond Code

MCP servers don't have to be coding-focused:
- **Creative tools**: Color palettes, design inspiration, writing prompts
- **Local data**: Search personal notes, bookmarks, project ideas
- **Lifestyle**: Coffee shop recommendations, transit info, event discovery
- **Productivity**: Time tracking, goal setting, habit monitoring
- **Fun**: Games, random generators, Easter eggs

### Quick Wins (1-2 hours)
- **Mood Board MCP**: Input "cozy autumn coding" → curated image links
- **Emoji Mapper MCP**: Add contextual emojis to any text
- **Commit Poem MCP**: Git commits → haikus or limericks  
- **Local Snippet Store**: Search/save code snippets by topic
- **Color Palette Generator**: From images, moods, or keywords

### Medium Complexity (2-4 hours)
- **Denver Explorer MCP**: Discover coffee shops, restaurants, events by neighborhood
- **Regex Builder MCP**: Plain English → working regex with test cases
- **Persona Generator MCP**: One-liner → complete UX persona with details
- **Learning Tracker MCP**: Track what you're learning with progress and insights
- **Weather + Vibes MCP**: Forecast paired with matching playlists

### Advanced (4+ hours)
- **Code Quality Analyzer**: Scan for patterns, suggest improvements with severity
- **API Design Assistant**: Natural language → REST endpoint specifications
- **Test Generator**: Function signatures → comprehensive test suites
- **Documentation Scanner**: Find undocumented code, suggest docs
- **Multi-source Aggregator**: Combine data from multiple APIs intelligently

---

## Demo Preparation

**Technical Setup:**
- [ ] Server starts without errors
- [ ] Cursor configuration (mcp.json) is correct
- [ ] All dependencies are installed and documented
- [ ] Response times are fast (< 2 seconds)

**Demo Content:**
- [ ] Clear 1-sentence pitch prepared
- [ ] 2-3 realistic use cases ready to show
- [ ] Sample queries tested and working

### Great Demo Structure (3-5 minutes)

**1. The Hook (30 seconds)**  
"Have you ever been frustrated by [problem]? I built a tool that solves this."

**2. Live Demo (2-3 minutes)**  
Show your server working in Cursor with 2-3 different use cases

**3. Why It's Special (30 seconds)**  
What makes your approach unique?

**4. Quick Code Walkthrough (optional)**  
Show one interesting implementation detail

---

## Resources

**Essential:**
- Cursor Docs: https://cursor.sh/docs
- FastMCP Docs: https://gofastmcp.com
- MCP Specification: https://spec.modelcontextprotocol.io
- FastMCP GitHub: https://github.com/jlowin/fastmcp

**Example Servers:**
- Official MCP Servers: https://github.com/modelcontextprotocol
- FastMCP Examples: https://github.com/jlowin/fastmcp/tree/main/examples

---

## Quick Reference

### MCP Core Concepts

**Tool**: A function the LLM can call with parameters
- Has a name, description, and input schema
- Receives JSON parameters, returns JSON result
- Should be focused on one task

**Resource**: Static or dynamic content the LLM can read (optional for most projects)

**Prompt**: Pre-built conversation starters or templates (optional)

### Essential MCP Methods

Your server must implement:
- `initialize` - Handshake with client
- `tools/list` - Return available tools
- `tools/call` - Execute a specific tool

---

## Let's Build!

**Start simple.** Pick one problem you've actually experienced. Build the smallest thing that solves it. Then polish.

**Make it real.** Tools that solve real problems always beat technically impressive demos of imaginary use cases.

**Have fun!** This is a chance to experiment with new technology and build something creative.

### Remember

A working demo of a simple, useful tool beats a complex, broken system every time.

The best projects come from scratching your own itch. What frustrates you? What would make your day better? Build that.

**Now go build something amazing!** 🚀
