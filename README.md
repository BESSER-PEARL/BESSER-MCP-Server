# BESSER-MCP-Server

A minimal Model Context Protocol (MCP) server implementation for [BESSER](https://github.com/BESSER-PEARL/BESSER), the Python-based low-code modeling platform.

## Overview

This MCP server provides access to BESSER's low-code platform modeling and code generation capabilities through the Model Context Protocol, enabling AI assistants and other MCP clients to interact with BESSER's features.

## Features
The BESSER MCP Server can be used both locally or deployed on a server.
To deploy it, the `--dist` or `-d` option needs to be added when starting the server
Both the local and distant implementation open the server on the following address: `http://127.0.0.1:8000/sse`.
However, the port can be changed through the `--port` or `-p` option.
Help on the server option can be printed using the `--help` or `-h` option.

The BESSER MCP Server provides the following tools:

- **Information tools:**
  - **`about`**: Get information about BESSER and this MCP server
  - **`get_model_info`**: Get detailed information about an existing domain model (classes, attributes, methods, relationships)
- **Creation tools:**
  - **`new_model`**: Create a new B-UML DomainModel with a specified name  
  - **`add_class`**: Add a new class in the model
  - **`add_method_to_class`**: Add a method to a given class
  - **`add_attribute_to_class`**: Add an attribute to a given class
  - **`add_binary_association`**: Add a binary association between two classes
  - **`add_association_class`**: Add an association class to an existing association
  - **`add_enumeration`**: Add an enumeration to the model
  - **`add_enumeration_literal`**: Add a literal to an enumeration
  - **`add_generalization`**: Add a generalization relation between two classes
  - **`add_ocl_constraint`**: Add an OCL constraint to a class
- **Deletion tools:**
  - **`delete_class`**: Remove a class from the model
  - **`delete_method_to_class`**: Remove a method from a given class
  - **`delete_attribute_to_class`**: Remove an attribute from a given class
  - **`delete_binary_association`**: Remove a binary association between two classes
  - **`delete_association_class`**: Remove an association class from an existing association
  - **`delete_enumeration`**: Remove an enumeration from the model
  - **`delete_enumeration_literal`**: Remove a literal from an enumeration
  - **`delete_generalization`**: Remove a generalization relation between two classes
  - **`delete_ocl_constraint`**: Remove an OCL constraint
- **Generation tools:**
  - **`sql_generation`**: Generate the SQL representation of the model
  - **`python_generation`**: Generate the set of Python classes implementing the model
  - **`backend_generation`**: Generate a backend implementation for the model
  - **`java_generation`**: Generate the set of Java classes implementing the model
  - **`json_schema_generation`**: Generate the JSON Schema of the model
  - **`json_smart_data_generation`**: Generate the Smart Data Schema for the model
  - **`pydantic_classes_generation`**: Generate a Pydentic representation of the model
  - **`rdf_generation`**: Generate the RDF vocabulary for the model
  - **`rest_api_generation`**: Generate a Rest API for the model
  - **`sql_alchemy_generation`**: Generate the SQLAlchemy code for the model

If the server is started locally, the server will directly access the file system for file generation.
If the server is distant, the generated code will be sent back to the LLM.
For this reason, generators producing multiple files are currently disabled in the distant mode.

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

To use this server with MCP clients like Claude Desktop, Cursor and Cline, you need to configure them to connect to the server.

#### Recommended setup (Cline)

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

##### Cline

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

##### Claude Desktop

1. **Locate the configuration directory:**
   - **macOS**: `~/Library/Application Support/Claude/`
   - **Windows**: `%APPDATA%\Claude\`

2. **Create or edit `claude_desktop_config.json`:**
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
       "besser-mcp": {
         "url": "http://127.0.0.1:8000/sse"
       }
     }
   }
   ```

### Testing the Connection

After configuring your MCP client:

1. **Start the server**
2. **Restart your MCP client**
3. **Test the connection** by asking:
   - "What is BESSER?" (uses the `about` tool)
   - "Create a new domain model called 'MyModel'" (uses `new_model`)
   - "Add a class named 'Person' to the model" (uses `add_class`)
   - "Show me information about the domain model" (uses `get_model_info`)
   - "Generate SQL from the domain model" (uses `sql_generation`)

[//]: # (### Validation)

[//]: # ()
[//]: # (You can verify the server setup using the provided test script:)

[//]: # ()
[//]: # (```bash)

[//]: # (python test_server_startup.py)

[//]: # (```)

## Configuration Files

The repository includes several pre-configured files to help with setup:

- `mcp-config.json` - Basic cross-platform configuration template
- `mcp-config-examples.json` - Multiple configuration examples  
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
3. **"Permission denied" errors**: Ensure the server script has appropriate permissions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
