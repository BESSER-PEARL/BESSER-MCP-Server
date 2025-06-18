# BESSER-MCP-Server

A minimal Model Context Protocol (MCP) server implementation for [BESSER](https://github.com/BESSER-PEARL/BESSER), the Python-based low-code modeling platform.

## Overview

This MCP server provides access to BESSER's low-code platform modeling and code generation capabilities through the Model Context Protocol, enabling AI assistants and other MCP clients to interact with BESSER's features.

## Features

The BESSER MCP Server provides the following tools:

- **`about`**: Get information about BESSER and this MCP server
- **`new_model`**: Create a new B-UML DomainModel with a specified name  
- **`add_class`**: Add a new Class to an existing DomainModel (with duplicate name detection)
- **`get_model_info`**: Get detailed information about an existing domain model (classes, attributes, methods, relationships)
- **`sql_generation`**: Generate SQL representation from a domain model using BESSER's SQL generator

## Prerequisites

Before using the MCP server, ensure you have:

- **Python 3.8+** installed
- **Required packages**:
  ```bash
  pip install mcp besser
  ```
  Or if using UV:
  ```bash
  uv add mcp besser
  ```

## Usage

### Running the Server

#### Production Mode

Run the MCP server directly:
```bash
python src/besser_mcp_server/server.py
```

Or install the package and run it:
```bash
pip install -e .
python -m besser_mcp_server.server
```

#### Development Mode

For development and debugging, use the MCP development server which includes the MCP inspector:
```bash
mcp dev src/besser_mcp_server/server.py
```

This will:
- Start the server in development mode
- Launch the MCP inspector in your browser for interactive testing
- Provide detailed logging and debugging information
- Allow you to test tools directly without configuring a client

### Configuring MCP Clients

To use this server with MCP clients like Claude Desktop or Cursor, you need to configure them to connect to the server.

#### Quick Setup (Windows)

Use the provided PowerShell installation script:

```powershell
# For Cursor IDE
.\install-mcp-config.ps1 -Client cursor

# For Claude Desktop
.\install-mcp-config.ps1 -Client claude

# For both clients
.\install-mcp-config.ps1 -Client both
```

#### Manual Configuration

##### Claude Desktop

1. **Locate the configuration directory:**
   - **macOS**: `~/Library/Application Support/Claude/`
   - **Windows**: `%APPDATA%\Claude\`

2. **Create or edit `claude_desktop_config.json`:**
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

##### Cursor IDE

1. **Create the Cursor MCP configuration directory:**
   ```bash
   mkdir -p ~/.cursor  # macOS/Linux
   # or
   mkdir %USERPROFILE%\.cursor  # Windows
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



### Testing the Connection

After configuring your MCP client:

1. **Restart your MCP client** (Claude Desktop or Cursor)
2. **Test the connection** by asking:
   - "What is BESSER?" (uses the `about` tool)
   - "Create a new domain model called 'MyModel'" (uses `new_model`)
   - "Add a class named 'Person' to the model" (uses `add_class`)
   - "Show me information about the domain model" (uses `get_model_info`)
   - "Generate SQL from the domain model" (uses `sql_generation`)

### Validation

You can verify the server setup using the provided test script:

```bash
python test_server_startup.py
```

## Configuration Files

The repository includes several pre-configured files to help with setup:

- `mcp-config.json` - Basic cross-platform configuration template
- `mcp-config-examples.json` - Advanced configuration examples  
- `claude-desktop-config-windows.json` - Windows-specific Claude Desktop config
- `cursor-mcp-config-windows.json` - Windows-specific Cursor config
- `install-mcp-config.ps1` - Automatic installation script for Windows

## Documentation

For detailed setup instructions and troubleshooting:

- `QUICK-START.md` - Fast setup guide
- `MCP-CLIENT-SETUP.md` - Comprehensive setup instructions with troubleshooting

## Example Usage

Once connected, you can interact with BESSER through natural language:

```
User: "Create a new domain model called 'ECommerceSystem'"
Assistant: [Uses new_model tool to create the model]

User: "Add a Customer class to the ECommerceSystem model"  
Assistant: [Uses add_class tool to add the Customer class]

User: "Add a Product class as well"
Assistant: [Uses add_class tool to add the Product class]

User: "Show me information about the current domain model"
Assistant: [Uses get_model_info tool to display model structure, classes, and relationships]

User: "Generate SQL from this domain model"
Assistant: [Uses sql_generation tool to create SQL representation]

User: "What is BESSER?"
Assistant: [Uses about tool to provide information about BESSER]
```

## Troubleshooting

### Common Issues

1. **"mcp is not found" or import errors**: 
   - Make sure you have the correct MCP package installed: `pip install mcp`
   - If you have an older version, upgrade it: `pip install --upgrade mcp`
   - Verify installation: `python -c "import mcp.server; print('MCP installed correctly')"`

2. **"Command not found" errors**: Ensure Python is in your system PATH
3. **"Module not found" errors**: Check that PYTHONPATH is set correctly in your configuration
4. **"Permission denied" errors**: Ensure the server script has appropriate permissions

### Debug Mode

To enable debug logging, add to your MCP client configuration:
```json
{
  "env": {
    "PYTHONPATH": "/path/to/project/src",
    "DEBUG": "true"
  }
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
