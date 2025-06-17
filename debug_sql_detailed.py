#!/usr/bin/env python3
"""Detailed debug script to examine SQL generator behavior."""

import asyncio
from besser_mcp_server.server import new_model, add_class

async def debug_sql_generator():
    """Debug the SQL generator directly."""
    from besser.generators.sql.sql_generator import SQLGenerator
    from besser.BUML.metamodel.structural import Property
    
    print("Creating new model...")
    model = await new_model("TestModel")
    
    print("Adding class...")
    model_with_class = await add_class(model, "EmptyClass")
    
    print("Getting classes...")
    classes = model_with_class.get_classes()
    
    print("Adding id attribute manually...")
    for cls in classes:
        if not cls.attributes:
            # Get the integer primitive type from the domain model
            int_type = None
            for data_type in model_with_class.types:
                if hasattr(data_type, 'name') and data_type.name == 'int':
                    int_type = data_type
                    break
            
            if int_type:
                # Create the "id" property with integer type
                id_property = Property(
                    name="id",
                    type=int_type,
                    multiplicity="1",
                    is_id=True
                )
                
                # Add the property to the class
                cls.attributes.add(id_property)
                print(f"Added id attribute to {cls.name}")
    
    print("Creating SQL generator...")
    sql_generator = SQLGenerator(model_with_class)
    
    print("Calling generate()...")
    sql_output = sql_generator.generate()
    
    print(f"SQL output type: {type(sql_output)}")
    print(f"SQL output repr: {repr(sql_output)}")
    print(f"SQL output length: {len(sql_output) if sql_output else 'None'}")
    
    if sql_output:
        print("SQL output content:")
        print("=" * 50)
        print(sql_output)
        print("=" * 50)
    else:
        print("SQL output is None or empty")
    
    # Try to examine the generator's internal state
    print(f"Generator model: {sql_generator.model}")
    print(f"Generator model classes: {list(sql_generator.model.get_classes())}")

if __name__ == "__main__":
    asyncio.run(debug_sql_generator()) 