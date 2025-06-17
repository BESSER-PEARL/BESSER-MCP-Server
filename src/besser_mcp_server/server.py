#!/usr/bin/env python3
"""
BESSER MCP Server - A minimal Model Context Protocol server for BESSER.

This module provides a complete MCP server implementation for BESSER's
low-code modeling platform capabilities.
"""

import asyncio
import logging
import sys
from typing import Any, Dict, List

from mcp.server import FastMCP

mcp = FastMCP("besser-mcp-server")

@mcp.tool()
def about() -> str:
    """Get information about BESSER and this MCP server."""
    return ("BESSER is a Python-based low-modeling low-code platform for smart and AI-enhanced software development. "
            "It provides modeling capabilities and code generation tools to help developers build software faster.\n\n"
            "Learn more about BESSER at: https://github.com/BESSER-PEARL/BESSER")

@mcp.tool()
async def add_class(
    domain_model,
    name: str,
    attributes=None,
    methods=None,
    is_abstract: bool = False,
    is_read_only: bool = False,
    behaviors=None,
    timestamp=None,
    metadata=None,
    is_derived: bool = False,
):
    """Adds a new `Class` instance to a B-UML DomainModel and returns the updated model.

    Args:
        domain_model (DomainModel): The B-UML domain model to extend.
        name (str): Name of the class.
        attributes (set[Property] | None): Attributes set (default None).
        methods (set[Method] | None): Methods set (default None).
        is_abstract (bool): Whether class is abstract.
        is_read_only (bool): Whether class is read-only.
        behaviors (set[BehaviorDeclaration] | None): Behaviors of the class.
        timestamp (datetime | None): Creation timestamp (defaults to *now*).
        metadata (Metadata | None): Arbitrary metadata.
        is_derived (bool): Whether the class element is derived.

    Returns:
        DomainModel | str: The same model instance with the new class, or an error message
                          if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import Class  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    if timestamp is None:
        timestamp = datetime.now(timezone.utc)

    # Default to empty sets if None provided
    attributes = attributes or set()
    methods = methods or set()
    behaviors = behaviors or set()

    new_class = Class(
        name=name,
        attributes=attributes,
        methods=methods,
        is_abstract=is_abstract,
        is_read_only=is_read_only,
        behaviors=behaviors,
        timestamp=timestamp,  # type: ignore[arg-type]
        metadata=metadata,
        is_derived=is_derived,
    )

    # Add the class through the proper helper to ensure all internal structures are updated
    try:
        domain_model.add_type(new_class)  # type: ignore[attr-defined]
        return domain_model
    except ValueError as e:
        # Return error message if class with same name already exists
        return f"Error adding class '{name}': {str(e)}"

@mcp.tool()
async def new_model(name: str):
    """Creates a new B-UML DomainModel with the specified name.

    Args:
        name (str): Name of the new domain model.

    Returns:
        DomainModel: A new domain model instance with the given name.
    """
    try:
        from besser.BUML.metamodel.structural import DomainModel  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    # Create and return a new DomainModel instance
    return DomainModel(name=name)

@mcp.tool()
async def sql_generation(domain_model):
    """Given a domain model, it creates a SQL representation of the model.

    Args:
        domain_model (DomainModel): The B-UML domain model to generate SQL from.

    Returns:
        str: SQL representation of the domain model, or an error message if generation fails.
    """
    try:
        from besser.generators.sql.sql_generator import SQLGenerator  # type: ignore
        from besser.BUML.metamodel.structural import Property  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library with SQL generator must be installed (`pip install besser`)."
        ) from exc

    try:
        # Check every class in the domain model and ensure it has at least one attribute
        classes = domain_model.get_classes()
        
        for cls in classes:
            if not cls.attributes:
                # Add an "id" attribute of type integer if the class has no attributes
                try:
                    # Get the integer primitive type from the domain model
                    int_type = None
                    for data_type in domain_model.types:
                        if hasattr(data_type, 'name') and data_type.name == 'int':
                            int_type = data_type
                            break
                    
                    if int_type:
                        # Create the "id" property with integer type
                        id_property = Property(
                            name="id",
                            type=int_type,
                            multiplicity="1",  # Single value
                            is_id=True  # Mark as identifier
                        )
                        
                        # Add the property to the class
                        cls.attributes.add(id_property)
                        
                except Exception as e:
                    # If we can't add the attribute, continue without it
                    # This ensures the tool doesn't fail completely
                    pass
        
        # Create SQL generator instance and generate SQL
        sql_generator = SQLGenerator(domain_model)
        sql_output = sql_generator.generate()
        
        # Check if sql_output is not None and not empty string
        if sql_output and sql_output.strip():
            return sql_output
        else:
            # Try to provide more detailed information about why no SQL was generated
            classes_info = []
            for cls in classes:
                attr_count = len(cls.attributes)
                classes_info.append(f"{cls.name} ({attr_count} attributes)")
            
            if not classes:
                return "No SQL generated. The domain model contains no classes."
            else:
                return f"No SQL generated. The domain model contains {len(classes)} class(es): {', '.join(classes_info)}. The SQL generator may require additional configuration or the classes may not meet SQL generation requirements."
            
    except Exception as e:
        # Return error message if SQL generation fails
        return f"Error generating SQL from domain model: {str(e)}"

if __name__ == "__main__":
    mcp.run() 

# ---------------------------------------------------------------------------
# Backward-compatibility alias (to be removed in a future major version)
# ---------------------------------------------------------------------------

# Alias using the old, non-PEP8 compliant name so existing integrations keep working
addClass = add_class  # pylint: disable=invalid-name 