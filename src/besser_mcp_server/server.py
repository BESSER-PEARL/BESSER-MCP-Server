#!/usr/bin/env python3
"""
BESSER MCP Server - A minimal Model Context Protocol server for BESSER.

This module provides a complete MCP server implementation for BESSER's
low-code modeling platform capabilities with serializable domain models.
"""
import argparse
import logging

from mcp.server import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = None

if __name__ == "__main__":
    from info import register_url_info_tools, register_base64_info_tools, register_info_tools
    from creation import register_url_creation_tools, register_base64_creation_tools, register_creation_tools
    from delete import register_url_deletion_tools, register_base64_deletion_tools, register_deletion_tools
    from generators import register_url_generator_tools, register_base64_generator_tools, register_generator_tools

    parser = argparse.ArgumentParser(
        prog='BESSER MCP Server',
        description='MCP Server to create B-UML models and use generators.')
    parser.add_argument("-d",'--dist', action='store_true',
                        help='Start the server in the distant mode')
    parser.add_argument("-p", '--port', default=8000, type=int,
                        help='Start the server in the distant mode')
    args = parser.parse_args()

    mcp = FastMCP("besser-mcp-server", port=args.port)

    if args.dist:
        register_url_info_tools(mcp, logger)
        register_url_creation_tools(mcp, logger)
        register_url_deletion_tools(mcp, logger)
        register_url_generator_tools(mcp, logger)
        register_base64_info_tools(mcp, logger)
        register_base64_creation_tools(mcp, logger)
        register_base64_deletion_tools(mcp, logger)
        register_base64_generator_tools(mcp, logger)
        mcp.run(transport="sse")
    else:
        register_info_tools(mcp, logger)
        register_creation_tools(mcp, logger)
        register_deletion_tools(mcp, logger)
        register_generator_tools(mcp, logger)
        mcp.run(transport="sse")

