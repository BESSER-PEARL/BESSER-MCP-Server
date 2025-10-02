import os

from src.besser_mcp_server.utils import deserialize_domain_model


def register_generator_tools(mcp, logger):
    @mcp.tool()
    async def sql_generation(domain_model_base64: str, sql_dialect: str = "sqlite") -> str:
        """Given a domain model as base64, it creates a SQL representation of the model.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            sql_dialect (str) : The SQL dialect of the output (default sqlite).

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
            sql_generator = SQLGenerator(domain_model, ".", sql_dialect)
            sql_generator.generate()

            try:
                with open(f"./tables_{sql_dialect}", "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                content = "\n".join(lines)
                os.remove(f"./tables_{sql_dialect}")
                return content

            except Exception as e:
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
                "BESSER library with Python generator must be installed (`pip install besser`)."
            ) from exc

        try:
            # Deserialize the domain model
            domain_model = deserialize_domain_model(domain_model_base64)

            # Create Python generator instance and generate Python
            python_generator = PythonGenerator(domain_model, ".")
            python_generator.generate()

            try:
                with open("./classes.py", "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                content = "\n".join(lines)
                os.remove("./classes.py")
                return content

            except Exception as e:
                # Try to provide more detailed information about why no Python was generated
                classes = domain_model.get_classes()
                classes_info = []
                for cls in classes:
                    attr_count = len(cls.attributes)
                    classes_info.append(f"{cls.name} ({attr_count} attributes)")

                if not classes:
                    return "No Python code generated. The domain model contains no classes."
                else:
                    return f"No Python code generated. The domain model contains {len(classes)} class(es): {', '.join(classes_info)}. The Python code generator may require additional configuration or the classes may not meet generation requirements."


        except Exception as e:
            # Return error message if Python generation fails
            return f"Error generating Python from domain model: {str(e)}"