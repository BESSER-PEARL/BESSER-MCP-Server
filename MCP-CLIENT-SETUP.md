# BESSER MCP Server - Client Setup Guide

This guide explains how to configure MCP clients (like Claude Desktop or Cursor) to connect to the BESSER MCP Server locally.

## Available Tools

The BESSER MCP Server provides the following tools:

- **`about`**: Get information about BESSER and this MCP server
- **`new_model`**: Create a new B-UML DomainModel with a specified name
- **`add_class`**: Add a new Class to an existing DomainModel

## Configuration Files

### Basic Configuration (`mcp-config.json`)

The simplest configuration for connecting to the BESSER MCP server:

```json
{
  "mcpServers": {
    "besser-mcp-server": {
      "command": "python",
      "args": [
        "src/besser_mcp_server/server.py"
      ],
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

### Advanced Configuration (`mcp-config-examples.json`)

Multiple configuration options for different environments:

1. **Python Direct**: Uses system Python directly
2. **UV Runner**: Uses UV package manager to run the server
3. **Module Mode**: Runs the server as a Python module

## Setup Instructions

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
       "besser-mcp-server": {
         "command": "python",
         "args": [
           "/full/path/to/BESSER-MCP-Server/src/besser_mcp_server/server.py"
         ],
         "env": {
           "PYTHONPATH": "/full/path/to/BESSER-MCP-Server/src"
         }
       }
     }
   }
   ```

4. **Replace `/full/path/to/BESSER-MCP-Server/` with your actual project path**

5. **Restart Claude Desktop**

### For Cursor IDE

1. **Create the Cursor MCP configuration directory:**
   ```bash
   mkdir -p ~/.cursor
   ```

2. **Create or edit `~/.cursor/mcp.json`:**
   ```json
   {
     "mcpServers": {
       "besser-mcp-server": {
         "command": "python",
         "args": [
           "/full/path/to/BESSER-MCP-Server/src/besser_mcp_server/server.py"
         ],
         "env": {
           "PYTHONPATH": "/full/path/to/BESSER-MCP-Server/src"
         }
       }
     }
   }
   ```

3. **Replace `/full/path/to/BESSER-MCP-Server/` with your actual project path**

4. **Restart Cursor**

## Configuration Options Explained

### Using System Python
```json
{
  "command": "python",
  "args": ["src/besser_mcp_server/server.py"],
  "env": {
    "PYTHONPATH": "src"
  }
}
```

### Using UV Package Manager
```json
{
  "command": "uv",
  "args": ["run", "python", "src/besser_mcp_server/server.py"]
}
```

### Using Python Module Mode
```json
{
  "command": "python",
  "args": ["-m", "besser_mcp_server.server"],
  "env": {
    "PYTHONPATH": "src"
  }
}
```

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

1. **Start your MCP client** (Claude Desktop or Cursor)
2. **Look for the BESSER MCP server** in the available tools/extensions
3. **Test the connection** by asking:
   - "What is BESSER?" (uses the `about` tool)
   - "Create a new domain model called 'MyModel'" (uses `new_model`)
   - "Add a class named 'Person' to the model" (uses `add_class`)

## Troubleshooting

### Common Issues

1. **"Command not found" errors:**
   - Ensure Python is in your system PATH
   - Use full paths in the configuration

2. **"Module not found" errors:**
   - Check that PYTHONPATH is set correctly
   - Verify the BESSER library is installed

3. **"Permission denied" errors:**
   - Ensure the server script has execute permissions
   - Check file paths are accessible

### Debug Mode

To enable debug logging, add to your configuration:
```json
{
  "env": {
    "PYTHONPATH": "src",
    "DEBUG": "true"
  }
}
```

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