"""
BESSER MCP Server - Model Context Protocol server implementation for BESSER.

This package provides MCP server functionality to interact with BESSER's
low-code modeling platform capabilities.
"""

__version__ = "0.1.0"
__author__ = "BESSER Team"
__email__ = "info@besser-pearl.org"

from .server import add_class, new_model, sql_generation, about  # re-export main tools for convenience

__all__ = ["add_class", "new_model", "sql_generation", "about"] 