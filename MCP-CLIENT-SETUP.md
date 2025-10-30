# BESSER MCP Server - Client Setup Guide

This guide explains how to configure MCP clients (like Claude Desktop or Cursor) to connect to the BESSER MCP Server locally.

## Configuration Files

### Configuration (`mcp-config.json`)

The configuration file for connecting to the BESSER MCP server:

```json
{
  "mcpServers": {
    "besser-mcp": {
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

## Setup Instructions

### For VScode Cline

1. Open the Cline panel on VScode
2. Click on "Manage MCP Server" at the bottom, then the cog
3. Clicking on "Configure MCP server" will open the configuration file
4. Add the "besser-mcp-server" in the "mcpServers" section:
   ```json
   {
     "mcpServers": {
       "besser-mcp": {
         "url": "http://127.0.0.1:8000/sse"
       }
     }
   }
   ```

### For Claude Desktop

1. **Locate the configuration directory:**
   - **macOS**: `~/Library/Application Support/Claude/`
   - **Windows**: `%APPDATA%\Claude\`

2. **Create or edit the `claude_desktop_config.json` file:**
   ```bash
   # macOS
   mkdir -p ~/Library/Application\ Support/Claude/
   
   # Windows (PowerShell)
   mkdir $env:APPDATA\Claude -Force
   ```

3. **Copy the configuration:**
   ```json
   {
     "mcpServers": {
       "besser-mcp": {
         "type": "sse",
         "url": "http://127.0.0.1:8000/sse"
       }
     }
   }
   ```

4. **Restart Claude Desktop**

### For Cursor IDE

1. **Create the Cursor MCP configuration directory:**
   ```bash
   mkdir -p ~/.cursor
   ```

2. **Create or edit `~/.cursor/mcp.json`:**
   ```json
   {
     "mcpServers": {
       "besser-mcp": {
         "url": "http://127.0.0.1:8000/sse"
       }
     }
   }
   ```

3. **Restart Cursor**

## Prerequisites

Before using the MCP server, ensure you have:

1. **Python 3.8+** installed
2. **BESSER library** installed:
   ```bash
   pip install besser
   ```
   Or if using UV:
   ```bash
   uv add besser
   ```

3. **FastMCP dependencies** installed:
   ```bash
   pip install fastmcp
   ```
   Or if using UV:
   ```bash
   uv add fastmcp
   ```

## Testing the Connection

After configuring your MCP client:

1. **Start your MCP client**
2. **Look for the BESSER MCP server** in the available tools/extensions
3. **Test the connection** by asking:
   - "What is BESSER?" (uses the `about` tool)
   - "Create a new domain model called 'MyModel'" (uses `new_model`)
   - "Add a class named 'Person' to the model" (uses `add_class`)

## Troubleshooting

### Common Issues

- **"Module not found" errors:**
   - Verify the BESSER library is installed

## Example Usage

Once connected, you can interact with the BESSER MCP server through natural language:

```
User: "Create a new domain model called 'ECommerceModel'"
Assistant: [Uses new_model tool to create the model]

User: "Add a Customer class to the model"
Assistant: [Uses add_class tool to add the Customer class]

User: "Tell me about BESSER"
Assistant: [Uses about tool to provide information]
```

The MCP server will handle the low-level BESSER library interactions while you work with natural language commands through your MCP client. 