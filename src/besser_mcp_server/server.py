#!/usr/bin/env python3
"""
BESSER MCP Server - A minimal Model Context Protocol server for BESSER.

This module provides a complete MCP server implementation for BESSER's
low-code modeling platform capabilities with serializable domain models.
"""

import asyncio
import base64
import io
import logging
import pickle
import sys
from typing import Any, Dict, List, Union

from mcp.server import FastMCP

from besser.BUML.metamodel.structural import Class, DomainModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("besser-mcp-server")

def serialize_domain_model(domain_model) -> str:
    """Convert a domain model to a base64 string using pickle."""
    try:
        
        # Serialize the domain model using pickle
        pickled_data = pickle.dumps(domain_model)
        
        # Convert to base64 for string representation
        encoded_data = base64.b64encode(pickled_data).decode('ascii')
        
        return encoded_data
                
    except Exception as e:
        logger.error(f"Error serializing model: {str(e)}")
        return f"Error serializing model: {str(e)}"

def deserialize_domain_model(model_base64: str):
    """Convert a base64 string back to a domain model object using pickle."""
    try:
        
        # Decode from base64
        pickled_data = base64.b64decode(model_base64.encode('ascii'))
        
        # Deserialize using pickle
        domain_model = pickle.loads(pickled_data)
        
        
        return domain_model
                
    except Exception as e:
        raise RuntimeError(f"Error deserializing model: {str(e)}")


@mcp.tool()
def about() -> str:
    """Get information about BESSER and this MCP server."""
    return ("BESSER is a Python-based low-modeling low-code platform for smart and AI-enhanced software development. "
            "It provides modeling capabilities and code generation tools to help developers build software faster.\n\n"
            "Learn more about BESSER at: https://github.com/BESSER-PEARL/BESSER")

@mcp.tool()
async def add_class(
    domain_model_base64: str,
    name: str,
    attributes=None,
    methods=None,
    is_abstract: bool = False,
    is_read_only: bool = False,
    behaviors=None,
    timestamp=None,
    metadata=None,
    is_derived: bool = False,
) -> str:
    """Adds a new `Class` instance to a B-UML DomainModel and returns the updated model as base64.

    Args:
        domain_model_base64 (str): The B-UML domain model as base64 string.
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
        str: The updated domain model as base64 string, or an error message
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

    try:
        logger.info(f"Adding class '{name}' to domain model")
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)
        
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
        )        # Check if a types with the same name already exists
        existing_classes = domain_model.get_classes()
        existing_class_names = {cls.name for cls in existing_classes}
        
        if name in existing_class_names:
            logger.warning(f"Class '{name}' already exists in model")
            return f"Error adding class '{name}': A class with name '{name}' already exists in the model"
        
        # Add the class directly to the types set to avoid BESSER's duplicate validation
        # which seems to have issues with primitive types
        try:
            domain_model.add_type(new_class)  # type: ignore[attr-defined]
            logger.info(f"Successfully added class '{name}' to model")
        except ValueError as ve:
            logger.warning(f"add_type failed, using direct addition")
            # If add_type fails due to duplicate primitive validation, add directly
            domain_model.types.add(new_class)  # type: ignore[attr-defined]
            logger.info(f"Successfully added class '{name}' to model using direct addition")
        
        # Return the updated model as base64
        return serialize_domain_model(domain_model)

    except ValueError as e:
        # Return error message if class with same name already exists
        return f"Error adding class '{name}': {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"


@mcp.tool()
async def add_method_to_class(
        domain_model_base64: str,
        name: str,
        class_name: str,
        visibility: str = "public",
        is_abstract: bool = False,
        parameters: set = set(),
        type_name:str = "str",
        code: str = "",
        timestamp = None,
        metadata = None,
        is_derived: bool = False
) -> str:
    """Adds a new method to a `Class` instance in a B-UML DomainModel and returns the updated model as base64.

    Args:
        domain_model_base64 (str): The B-UML domain model as base64 string.
        name (str): The name of the method.
        class_name (str): The name of the class that will contain the method.
        visibility (str): Determines the kind of visibility of the method (public as default).
        is_abstract (bool): Indicates if the method is abstract (False as default).
        parameters (set[Parameter]): The set of parameters for the method (set() as default).
        type_name (str): The name of the type of the method ("str" as default).
        code (str): code of the method ("" as default).
        timestamp (datetime): Object creation datetime (default is current time).
        metadata (Metadata): Metadata information for the method (None as default).
        is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

    Returns:
        str: The updated domain model as base64 string, or an error message
             if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import Method  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    try:
        logger.info(f"Adding method '{name}' to class '{class_name}'")
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)


        owner = domain_model.get_type_by_name(class_name)
        existing_methods = owner.methods
        existing_method_names = {method.name for method in existing_methods}

        method_type = domain_model.get_type_by_name(type_name)

        if name in existing_method_names:
            logger.warning(f"Method '{name}' already exists in Class '{class_name}'")
            return f"Error adding method '{name}': A method with name '{name}' already exists in the class '{class_name}'"

        new_method = Method(
            name,
            visibility,
            is_abstract,
            parameters,
            method_type,
            owner,
            code,
            timestamp,  # type: ignore[arg-type]
            metadata,
            is_derived
        )

        owner.add_method(new_method)
        logger.info(f"Successfully added method '{name}' to class '{class_name}'")

        # Return the updated model as base64
        return serialize_domain_model(domain_model)

    except ValueError as e:
        # Return error message if class with same name already exists
        return f"Error adding method '{name}' to class '{class_name}': {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"


@mcp.tool()
async def add_attribute_to_class(
        domain_model_base64: str,
        name: str,
        class_name: str,
        type_name,
        multiplicity,
        visibility,
        is_composite,
        is_navigable,
        is_id,
        is_read_only,
        timestamp,
        metadata,
        is_derived,
) -> str:
    """Adds a new attribute to a `Class` instance in a B-UML DomainModel and returns the updated model as base64.

    Args:
        domain_model_base64 (str): The B-UML domain model as base64 string.
        name (str): The name of the property.
        class_name (str): The name of the class that will contain the attribute.
        type_name (str): The type of the property.
        multiplicity (Multiplicity): The multiplicity of the property (1..1 as default).
        visibility (str): The visibility of the property (public as default).
        is_composite (bool): Indicates whether the property is a composite (False as default).
        is_navigable (bool): Indicates whether the property is navigable in a relationship (True as default).
        is_id (bool): Indicates whether the property is an id (False as default).
        is_read_only (bool): Indicates whether the property is read only (False as default).
        timestamp (datetime): Object creation datetime (default is current time).
        metadata (Metadata): Metadata information for the property (None as default).
        is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

    Returns:
        str: The updated domain model as base64 string, or an error message
             if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import Property  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    try:
        logger.info(f"Adding method '{name}' to class '{class_name}'")
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        owner = domain_model.get_type_by_name(class_name)
        existing_attributes = owner.attributes
        existing_attribute_names = {attribute.name for attribute in existing_attributes}

        property_type = domain_model.get_type_by_name(type_name)

        if name in existing_attribute_names:
            logger.warning(f"Attribute '{name}' already exists in Class '{class_name}'")
            return f"Error adding attribute '{name}': An attribute with name '{name}' already exists in the class '{class_name}'"

        new_property = Property(
            name,
            property_type,
            owner,
            multiplicity,
            visibility,
            is_composite,
            is_navigable,
            is_id,
            is_read_only,
            timestamp, # type: ignore[arg-type]
            metadata,
            is_derived,
        )

        owner.add_attribute(new_property)
        logger.info(f"Successfully added attribute '{name}' to class '{class_name}'")

        # Return the updated model as base64
        return serialize_domain_model(domain_model)

    except ValueError as e:
        # Return error message if class with same name already exists
        return f"Error adding attribute '{name}' to class '{class_name}': {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"



@mcp.tool()
async def new_model(name: str) -> str:
    """Creates a new B-UML DomainModel with the specified name and returns it as base64.

    Args:
        name (str): Name of the new domain model.

    Returns:
        str: A new domain model instance as base64 string.
    """
    try:
        from besser.BUML.metamodel.structural import DomainModel  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    # Create and return a new DomainModel instance as base64
    domain_model = DomainModel(name=name)
    return serialize_domain_model(domain_model)

@mcp.tool()
async def sql_generation(domain_model_base64: str) -> str:
    """Given a domain model as base64, it creates a SQL representation of the model.

    Args:
        domain_model_base64 (str): The B-UML domain model as base64 string.

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
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)
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


@mcp.tool()
async def python_generation(domain_model_base64: str) -> str:
    """Given a domain model as base64, it creates a set of python classes implementing the model.

    Args:
        domain_model_base64 (str): The B-UML domain model as base64 string.

    Returns:
        str: Python representation of the domain model, or an error message if generation fails.
    """
    try:
        from besser.generators.python_classes.python_classes_generator import PythonGenerator  # type: ignore
        from besser.BUML.metamodel.structural import Property  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library with SQL generator must be installed (`pip install besser`)."
        ) from exc

    try:
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        # Create SQL generator instance and generate SQL
        python_generator = PythonGenerator(domain_model)
        python_output = python_generator.generate()

        # Check if sql_output is not None and not empty string
        if python_output and python_output.strip():
            return python_output

    except Exception as e:
        # Return error message if SQL generation fails
        return f"Error generating SQL from domain model: {str(e)}"

@mcp.tool()
async def get_model_info(domain_model_base64: str) -> str:
    """Get detailed information about a domain model.

    Args:
        domain_model_base64 (str): The B-UML domain model as base64 string.

    Returns:
        str: Detailed information about the domain model.
    """
    try:
        logger.info("Getting model info")
        domain_model = deserialize_domain_model(domain_model_base64)
        classes = domain_model.get_classes()
        
        info = [f"Domain Model: {domain_model.name}"]
        info.append(f"Total types: {len(domain_model.types)}")
        info.append(f"Classes: {len(classes)}")
        
        if classes:
            info.append("Class details:")
            for cls in classes:
                info.append(f"  - {cls.name} ({len(cls.attributes)} attributes)")
                for attr in cls.attributes:
                    attr_type = attr.type.name if hasattr(attr.type, 'name') else str(attr.type)
                    info.append(f"    * {attr.name}: {attr_type}")
        
        return "\n".join(info)
    except Exception as e:
        return f"Error getting model info: {str(e)}"

if __name__ == "__main__":
    mcp.run() 

