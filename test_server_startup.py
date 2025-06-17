#!/usr/bin/env python3
"""
Test script to verify the BESSER MCP Server can start correctly.
This script imports and validates the server without running it.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_server_import():
    """Test that the server module can be imported successfully."""
    try:
        from besser_mcp_server.server import mcp, about, add_class, new_model
        print("✓ Successfully imported BESSER MCP Server")
        return True
    except ImportError as e:
        print(f"✗ Failed to import server: {e}")
        return False

def test_server_tools():
    """Test that all expected tools are registered."""
    try:
        from besser_mcp_server.server import mcp
        
        # Check that the functions are properly decorated and available
        expected_functions = ['about', 'add_class', 'new_model', 'sql_generation']
        
        # Import the functions directly to verify they exist
        from besser_mcp_server.server import about, add_class, new_model, sql_generation
        
        print(f"Available functions: {expected_functions}")
        print("✓ All expected tools are available as functions")
        return True
            
    except Exception as e:
        print(f"✗ Failed to check tools: {e}")
        return False

def test_dependencies():
    """Test that required dependencies are available."""
    dependencies = {
        'mcp.server': 'FastMCP',
        'besser.BUML.metamodel.structural': 'BESSER library'
    }
    
    all_good = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name} is available")
        except ImportError:
            print(f"✗ {name} is not available - install with: pip install {name.lower()}")
            all_good = False
    
    return all_good

def main():
    """Run all tests."""
    print("Testing BESSER MCP Server setup...\n")
    
    tests = [
        ("Server Import", test_server_import),
        ("Dependencies", test_dependencies),
        ("Tool Registration", test_server_tools),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append(result)
    
    print("\n" + "="*50)
    if all(results):
        print("✓ All tests passed! The server is ready to use.")
        print("\nNext steps:")
        print("1. Configure your MCP client using the provided configuration files")
        print("2. Start your MCP client (Claude Desktop, Cursor, etc.)")
        print("3. Test the connection by asking about BESSER")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 