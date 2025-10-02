#!/usr/bin/env python3
"""
BESSER MCP Server - A minimal Model Context Protocol server for BESSER.

This module provides a complete MCP server implementation for BESSER's
low-code modeling platform capabilities with serializable domain models.
"""

import logging

from mcp.server import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("besser-mcp-server", stateless_http=True)

if __name__ == "__main__":
    from src.besser_mcp_server.info import register_info_tools
    from src.besser_mcp_server.creation import register_creation_tools
    from src.besser_mcp_server.delete import register_deletion_tools
    from src.besser_mcp_server.generators import register_generator_tools

    register_info_tools(mcp, logger)
    register_creation_tools(mcp, logger)
    register_deletion_tools(mcp, logger)
    register_generator_tools(mcp, logger)
    mcp.run(transport="streamable-http")
    # mcp.run()

