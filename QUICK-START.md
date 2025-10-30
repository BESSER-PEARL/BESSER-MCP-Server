# BESSER MCP Server - Quick Start Guide

This guide provides the fastest way to get the BESSER MCP Server running with your favorite MCP client.
The recommended setup to use the BESSER MCP Server freely is through Cline with a free to use model from OpenRouter.

## Recommended Setup (VScode with Cline)

1. Open the Cline panel on VScode
2. Click on "Manage MCP Server" at the bottom, then the cog
3. Clicking on "Configure MCP server" will open the configuration file
4. Copy `mcp-config.json` content to the opened config file

## 🚀 Quick Setup (Windows Automatic Installation)

Run the PowerShell installation script:

```powershell
# For Cursor IDE
.\install-mcp-config.ps1 -Client cursor

# For Claude Desktop
.\install-mcp-config.ps1 -Client claude

# For both clients
.\install-mcp-config.ps1 -Client both
```

## Manual Configuration

### For VScode Cline:
1. Open the Cline panel on VScode
2. Click on "Manage MCP Server" at the bottom, then the cog
3. Clicking on "Configure MCP server" will open the configuration file
4. Copy `mcp-config.json` content to the opened config file

### For Cursor IDE:
1. Copy `cursor-mcp-config-windows.json` content to `~/.cursor/mcp.json`
2. Update paths if your project is in a different location

### For Claude Desktop:
1. Copy `claude-desktop-config-windows.json` content to `%APPDATA%\Claude\claude_desktop_config.json`
2. Update paths if your project is in a different location

## 📁 Available Configuration Files

| File | Purpose                                     |
|------|---------------------------------------------|
| `mcp-config.json` | Basic cross-platform configuration template |
| `mcp-config-examples.json` | Multiple configuration examples             |
| `claude-desktop-config-windows.json` | Windows-specific Claude Desktop config      |
| `cursor-mcp-config-windows.json` | Windows-specific Cursor config              |
| `install-mcp-config.ps1` | Automatic installation script for Windows   |

[//]: # (## 🛠️ Available Tools)

[//]: # ()
[//]: # (Once connected, you can use these tools through natural language:)

[//]: # ()
[//]: # (| Tool | Description | Example Usage |)

[//]: # (|------|-------------|---------------|)

[//]: # (| `about` | Get information about BESSER | "What is BESSER?" |)

[//]: # (| `new_model` | Create a new domain model | "Create a new model called 'ECommerce'" |)

[//]: # (| `add_class` | Add a class to a model | "Add a Customer class to the model" |)

## ✅ Testing Your Setup

1. **Server startup:**
   ```bash
   python server.py
   ```

2. **Test in your MCP client:**
   - Restart your MCP client (Cursor/Claude Desktop)
   - Ask: "What is BESSER?"
   - Try: "Create a new domain model called 'TestModel'"
   - Try: "Add a Person class to the model"

## 📋 Prerequisites

Make sure you have:
- Python 3.8+
- Required packages:
  ```bash
  pip install mcp besser
  ```

## 🔧 Troubleshooting

### Common Issues:

1. **"Command not found"**: Ensure Python is in your PATH
2. **"Module not found"**: Check PYTHONPATH in configuration
3. **"Permission denied"**: Run PowerShell as Administrator


## 📖 Full Documentation

For detailed setup instructions and advanced configuration options, see:
- `MCP-CLIENT-SETUP.md` - Complete setup guide
- `README.md` - Project overview

## 💡 Example Workflow

```
1. User: "Create a new domain model called 'LibrarySystem'"
   → Server uses new_model tool

2. User: "Add a Book class to the LibrarySystem model"
   → Server uses add_class tool

3. User: "Add an Author class as well"
   → Server uses add_class tool again

4. User: "What is BESSER again?"
   → Server uses about tool
```

The BESSER MCP Server handles all the complex BESSER library interactions while you work with simple, natural language commands! 