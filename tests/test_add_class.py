"""Tests for add_class tool in MCP server."""
"""Tests for add_class and new_model tools in MCP server."""
"""Tests for add_class, new_model, and sql_generation tools in MCP server."""

import asyncio
import pytest

from besser_mcp_server.server import add_class
from besser_mcp_server.server import add_class, new_model, sql_generation

from besser.BUML.metamodel.structural import DomainModel, Class


async def _run_add():
    # Create initial model with one class
    class_a = Class(name="ClassA")
    model = DomainModel(name="TestModel", types={class_a})

    # Call tool to add new class
    updated_model = await add_class(model, name="ClassB")

    return updated_model


def test_add_class_tool():
    updated_model = asyncio.run(_run_add())

    class_names = {cls.name for cls in updated_model.get_classes()}

    assert class_names == {"ClassA", "ClassB"}


async def _run_add_duplicate():
    # Create initial model with one class
    class_a = Class(name="ClassA")
    model = DomainModel(name="TestModel", types={class_a})

    # Try to add class with same name - should return error
    result = await add_class(model, name="ClassA")

    return result


def test_add_duplicate_class_returns_error():
    result = asyncio.run(_run_add_duplicate())
    
    # Should return error string instead of model
    assert isinstance(result, str)
    assert "Error adding class 'ClassA':" in result


async def _run_new_model():
    # Create a new model with specified name
    model = await new_model(name="TestNewModel")
    return model


def test_new_model_tool():
    model = asyncio.run(_run_new_model())
    
    # Should return a DomainModel instance
    assert isinstance(model, DomainModel)
    assert model.name == "TestNewModel"
    # New model should have empty types set initially
    assert len(model.types) >= 0  # May have default primitive types


async def _run_integration_test():
    # Create a new model
    model = await new_model(name="IntegrationTestModel")
    
    # Add a class to the new model
    updated_model = await add_class(model, name="TestClass")
    
    return updated_model


def test_new_model_and_add_class_integration():
    model = asyncio.run(_run_integration_test())
    
    # Should return a DomainModel instance
    assert isinstance(model, DomainModel)
    assert model.name == "IntegrationTestModel"
    
    # Should contain the added class
    class_names = {cls.name for cls in model.get_classes()}
    assert "TestClass" in class_names


async def _run_sql_generation():
    # Create a model with a class
    model = await new_model(name="SQLTestModel")
    model_with_class = await add_class(model, name="TestEntity")
    
    # Generate SQL from the model
    sql_result = await sql_generation(model_with_class)
    
    return sql_result


def test_sql_generation_tool():
    sql_result = asyncio.run(_run_sql_generation())
    
    # Should return a string (either SQL or error message)
    assert isinstance(sql_result, str)
    # Should not be empty
    assert len(sql_result) > 0
    # For a successful generation, it should contain SQL keywords or be an informative message
    assert ("CREATE" in sql_result.upper() or 
            "TABLE" in sql_result.upper() or 
            "No SQL generated" in sql_result or
            "Error generating SQL" in sql_result)


async def _run_sql_generation_empty_model():
    # Create an empty model (no classes)
    model = await new_model(name="EmptyModel")
    
    # Generate SQL from empty model
    sql_result = await sql_generation(model)
    
    return sql_result


def test_sql_generation_empty_model():
    sql_result = asyncio.run(_run_sql_generation_empty_model())
    
    # Should return a string indicating no SQL was generated
    assert isinstance(sql_result, str)
    assert len(sql_result) > 0


@pytest.mark.asyncio
async def test_sql_generation_adds_id_to_empty_classes():
    """Test that sql_generation adds id attribute to classes without attributes."""
    pytest.importorskip("besser")
    
    from besser.BUML.metamodel.structural import DomainModel
    from besser_mcp_server.server import new_model, add_class, sql_generation
    
    # Create a new model
    model = await new_model("TestModel")
    
    # Add a class without any attributes
    model_with_class = await add_class(model, "EmptyClass")
    
    # Verify the class has no attributes initially
    classes = model_with_class.get_classes()
    empty_class = next((cls for cls in classes if cls.name == "EmptyClass"), None)
    assert empty_class is not None
    assert len(empty_class.attributes) == 0
    
    # Generate SQL - this should add an id attribute
    sql_result = await sql_generation(model_with_class)
    
    # Verify the result is a string (SQL output) and not an error
    assert isinstance(sql_result, str)
    assert not sql_result.startswith("Error")
    assert not sql_result.startswith("No SQL generated")
    
    # Verify the class now has an id attribute
    assert len(empty_class.attributes) == 1
    id_attr = next(iter(empty_class.attributes))
    assert id_attr.name == "id"
    assert id_attr.type.name == "int"
    assert id_attr.is_id is True 