#!/usr/bin/env python3
"""Debug script to test sql_generation functionality."""

import asyncio
from besser_mcp_server.server import new_model, add_class, sql_generation

async def debug_sql_generation():
    """Debug the SQL generation process."""
    print("Creating new model...")
    model = await new_model("TestModel")
    print(f"Model created: {model}")
    print(f"Model types: {list(model.types)}")
    
    print("\nAdding class...")
    model_with_class = await add_class(model, "EmptyClass")
    print(f"Model with class: {model_with_class}")
    
    print("\nChecking classes...")
    classes = model_with_class.get_classes()
    print(f"Classes: {list(classes)}")
    
    for cls in classes:
        print(f"Class {cls.name}: attributes = {list(cls.attributes)}")
    
    print("\nGenerating SQL...")
    sql_result = await sql_generation(model_with_class)
    print(f"SQL result: {sql_result}")
    
    print("\nChecking classes after SQL generation...")
    for cls in classes:
        print(f"Class {cls.name}: attributes = {list(cls.attributes)}")
        for attr in cls.attributes:
            print(f"  - {attr.name}: {attr.type} (type name: {attr.type.name if hasattr(attr.type, 'name') else 'no name'})")

if __name__ == "__main__":
    asyncio.run(debug_sql_generation()) 