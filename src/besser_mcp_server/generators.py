import os

from besser.BUML.metamodel.structural import DomainModel
from utils import deserialize_domain_model, download_model_from, get_model


def base_sql_generation(domain_model: DomainModel, sql_dialect: str = "sqlite", path: str = "."):
    """Given a domain model, it creates a SQL representation of the model.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        sql_dialect (str) : The SQL dialect of the output (default sqlite).
        path (str): The generation path

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
        sql_generator = SQLGenerator(domain_model, path, sql_dialect)
        sql_generator.generate()

    except Exception as e:
        # Return error message if SQL generation fails
        return f"Error generating SQL from domain model: {str(e)}"


def base_python_generation(domain_model: DomainModel, path: str = "."):
    """Given a domain model, it creates a set of python classes implementing the model.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        path (str) : the generation path

    Returns:
        str: Python representation of the domain model, or an error message if generation fails.
    """
    try:
        from besser.generators.python_classes.python_classes_generator import PythonGenerator  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library with Python generator must be installed (`pip install besser`)."
        ) from exc

    try:
        # Create Python generator instance and generate Python
        python_generator = PythonGenerator(domain_model, path)
        python_generator.generate()

    except Exception as e:
        # Return error message if Python generation fails
        return f"Error generating Python from domain model: {str(e)}"


def base_backend_generation(domain_model: DomainModel, path:str = "."):
    """Given a domain model, it creates a backend for the model.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        path (str) : the generation path
    """
    try:
        from besser.generators.backend.backend_generator import BackendGenerator  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library with Backend generator must be installed (`pip install besser`)."
        ) from exc

    try:
        # Create Backend generator instance and generate the backend
        backend_generator = BackendGenerator(domain_model, output_dir=path)
        backend_generator.generate()

    except Exception as e:
        # Return error message if Backend generation fails
        return f"Error generating Backend from domain model: {str(e)}"


def base_java_generation(domain_model: DomainModel, path:str = "."):
    """Given a domain model, it creates a set of Java classes implementing the model.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        path (str) : the generation path
    """
    try:
        from besser.generators.java_classes.java_generator import JavaGenerator  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library with Java generator must be installed (`pip install besser`)."
        ) from exc

    try:
        # Create Java generator instance and generate Java
        java_generator = JavaGenerator(domain_model, output_dir=path)
        java_generator.generate()

    except Exception as e:
        # Return error message if Java generation fails
        return f"Error generating Java from domain model: {str(e)}"

def base_json_generation(domain_model: DomainModel, path:str = ".", mode="regular"):
    """Given a domain model, it creates the corresponding JSON Schema or Smart Data schema.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        path (str) : the generation path
        mode (str) : mode of generation (regular or smart_data)
    """
    try:
        from besser.generators.json.json_schema_generator import JSONSchemaGenerator  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library with Backend generator must be installed (`pip install besser`)."
        ) from exc

    try:
        # Create JSONSchema generator instance and generate JSON Schema
        json_generator = JSONSchemaGenerator(domain_model, output_dir=path, mode=mode)
        json_generator.generate()

    except Exception as e:
        # Return error message if JSON Schema generation fails
        return f"Error generating JSON Schema from domain model: {str(e)}"


def base_pydantic_classes_generation(domain_model: DomainModel, path:str = "."):
    """Given a domain model, it creates a set of python classes implementing the model.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        path (str) : the generation path
    """
    try:
        from besser.generators.pydantic_classes.pydantic_classes_generator import PydanticGenerator  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library with Pydantic generator must be installed (`pip install besser`)."
        ) from exc

    try:
        # Create Pydantic generator instance and generate Pydantic
        pydantic_classes_generator = PydanticGenerator(domain_model, output_dir=path)
        pydantic_classes_generator.generate()

    except Exception as e:
        # Return error message if Pydantic generation fails
        return f"Error generating Pydantic from domain model: {str(e)}"

def base_rdf_generation(domain_model: DomainModel, path:str = "."):
    """Given a domain model, it creates a set of python classes implementing the model.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        path (str) : the generation path
    """
    try:
        from besser.generators.rdf.rdf_generator import RDFGenerator  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library with RDF generator must be installed (`pip install besser`)."
        ) from exc

    try:
        # Create RDF generator instance and generate RDF
        rdf_generator = RDFGenerator(domain_model, output_dir=path)
        rdf_generator.generate()

    except Exception as e:
        # Return error message if RDF generation fails
        return f"Error generating RDF from domain model: {str(e)}"

def base_rest_api_generation(domain_model: DomainModel, path:str = "."):
    """Given a domain model, it creates a set of python classes implementing the model.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        path (str) : the generation path
    """
    try:
        from besser.generators.rest_api.rest_api_generator import RESTAPIGenerator  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library with RESTAPI generator must be installed (`pip install besser`)."
        ) from exc

    try:
        # Create RESTAPI generator instance and generate RESTAPI
        rest_api_generator = RESTAPIGenerator(domain_model, output_dir=path)
        rest_api_generator.generate()

    except Exception as e:
        # Return error message if RESTAPI generation fails
        return f"Error generating RESTAPI from domain model: {str(e)}"

def base_sql_alchemy_generation(domain_model: DomainModel, path:str = "."):
    """Given a domain model, it creates a set of python classes implementing the model.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        path (str) : the generation path
    """
    try:
        from besser.generators.sql_alchemy.sql_alchemy_generator import SQLAlchemyGenerator  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library with SQLAlchemy generator must be installed (`pip install besser`)."
        ) from exc

    try:
        # Create SQLAlchemy generator instance and generate SQLAlchemy
        sql_alchemy_generator = SQLAlchemyGenerator(domain_model, output_dir=path)
        sql_alchemy_generator.generate()

    except Exception as e:
        # Return error message if SQLAlchemy generation fails
        return f"Error generating SQLAlchemy from domain model: {str(e)}"

def register_base64_generator_tools(mcp, logger):
    @mcp.tool()
    def sql_generation_base64(domain_model_base64: str, sql_dialect: str = "sqlite") -> str:
        """Given a domain model as base64, it creates a SQL representation of the model.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            sql_dialect (str) : The SQL dialect of the output (default sqlite).

        Returns:
            str: SQL representation of the domain model, or an error message if generation fails.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)
        out = base_sql_generation(domain_model, sql_dialect)
        if out is not None:
            return out
        try:
            with open(f"./tables_{sql_dialect}", "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            content = "\n".join(lines)
            os.remove(f"./tables_{sql_dialect}")
            return content

        except Exception as e:
            # Try to provide more detailed information about why no SQL was generated
            classes = domain_model.get_classes()
            classes_info = []
            for cls in classes:
                attr_count = len(cls.attributes)
                classes_info.append(f"{cls.name} ({attr_count} attributes)")

            if not classes:
                return "No SQL generated. The domain model contains no classes."
            else:
                return f"No SQL generated. The domain model contains {len(classes)} class(es): {', '.join(classes_info)}. The SQL generator may require additional configuration or the classes may not meet SQL generation requirements."




    @mcp.tool()
    def python_generation_base64(domain_model_base64: str) -> str:
        """Given a domain model as base64, it creates a set of python classes implementing the model.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.

        Returns:
            str: Python representation of the domain model, or an error message if generation fails.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)
        out = base_python_generation(domain_model)
        if out is not None:
            return out
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

    @mcp.tool()
    def json_schema_generation_base64(domain_model_base64: str) -> str:
        """Given a domain model as base64, creates the JSON Schema representing the model.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.

        Returns:
            str: JSON schema of the domain model, or an error message if generation fails.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)
        out = base_json_generation(domain_model)
        if out is not None:
            return out
        try:
            with open("./schema.json", "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            content = "\n".join(lines)
            os.remove("./schema.json")
            return content

        except Exception as e:
            # Try to provide more detailed information about why no JSON Schema was generated
            classes = domain_model.get_classes()
            classes_info = []
            for cls in classes:
                attr_count = len(cls.attributes)
                classes_info.append(f"{cls.name} ({attr_count} attributes)")

            if not classes:
                return "No JSON Schema generated. The domain model contains no classes."
            else:
                return f"No JSON Schema generated. The domain model contains {len(classes)} class(es): {', '.join(classes_info)}. The JSON Schema generator may require additional configuration or the classes may not meet generation requirements."

    @mcp.tool()
    def rdf_generation_base64(domain_model_base64: str) -> str:
        """Given a domain model as base64, it creates the RDF Vocabulary for the model.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.

        Returns:
            str: RDF Vocabulary of the domain model, or an error message if generation fails.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)
        out = base_rdf_generation(domain_model)
        if out is not None:
            return out
        try:
            with open("./vocabulary.ttl", "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            content = "\n".join(lines)
            os.remove("./vocabulary.ttl")
            return content

        except Exception as e:
            # Try to provide more detailed information about why no RDF was generated
            classes = domain_model.get_classes()
            classes_info = []
            for cls in classes:
                attr_count = len(cls.attributes)
                classes_info.append(f"{cls.name} ({attr_count} attributes)")

            if not classes:
                return "No RDF Vocabulary generated. The domain model contains no classes."
            else:
                return f"No RDF Vocabulary generated. The domain model contains {len(classes)} class(es): {', '.join(classes_info)}. The RDF Vocabulary generator may require additional configuration or the classes may not meet generation requirements."


def register_url_generator_tools(mcp, logger):
    @mcp.tool()
    def sql_generation_with_url(domain_model_url: str, sql_dialect: str = "sqlite") -> str:
        """Given a domain model pointed by the passed URL, it creates a SQL representation of the model.

        Args:
            domain_model_url (str): The B-UML domain model URL location.
            sql_dialect (str) : The SQL dialect of the output (default sqlite).

        Returns:
            str: SQL representation of the domain model, or an error message if generation fails.
        """
        # Get the model
        serialized_domain_model = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(serialized_domain_model)
        out = base_sql_generation(domain_model, sql_dialect)
        if out is not None:
            return out
        try:
            with open(f"./tables_{sql_dialect}", "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            content = "\n".join(lines)
            os.remove(f"./tables_{sql_dialect}")
            return content

        except Exception as e:
            # Try to provide more detailed information about why no SQL was generated
            classes = domain_model.get_classes()
            classes_info = []
            for cls in classes:
                attr_count = len(cls.attributes)
                classes_info.append(f"{cls.name} ({attr_count} attributes)")

            if not classes:
                return "No SQL generated. The domain model contains no classes."
            else:
                return f"No SQL generated. The domain model contains {len(classes)} class(es): {', '.join(classes_info)}. The SQL generator may require additional configuration or the classes may not meet SQL generation requirements."




    @mcp.tool()
    def python_generation_with_url(domain_model_url: str) -> str:
        """Given a domain model pointed by the passed URL, it creates a set of python classes implementing the model.

        Args:
            domain_model_url (str): The B-UML domain model URL location.

        Returns:
            str: Python representation of the domain model, or an error message if generation fails.
        """
        # Get the model
        serialized_domain_model = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(serialized_domain_model)
        out = base_python_generation(domain_model)
        if out is not None:
            return out
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

    @mcp.tool()
    def json_schema_generation_with_url(domain_model_url: str) -> str:
        """Given a domain model pointed by the passed URL, creates the JSON Schema representing the model.

        Args:
            domain_model_url (str): The B-UML domain model URL location.

        Returns:
            str: JSON schema of the domain model, or an error message if generation fails.
        """
        # Get the model
        serialized_domain_model = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(serialized_domain_model)
        out = base_json_generation(domain_model)
        if out is not None:
            return out
        try:
            with open("./schema.json", "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            content = "\n".join(lines)
            os.remove("./schema.json")
            return content

        except Exception as e:
            # Try to provide more detailed information about why no JSON Schema was generated
            classes = domain_model.get_classes()
            classes_info = []
            for cls in classes:
                attr_count = len(cls.attributes)
                classes_info.append(f"{cls.name} ({attr_count} attributes)")

            if not classes:
                return "No JSON Schema generated. The domain model contains no classes."
            else:
                return f"No JSON Schema generated. The domain model contains {len(classes)} class(es): {', '.join(classes_info)}. The JSON Schema generator may require additional configuration or the classes may not meet generation requirements."

    @mcp.tool()
    def rdf_generation_with_url(domain_model_url: str) -> str:
        """Given a domain model pointed by the passed URL, creates the RDF vocabulary for the model.

        Args:
            domain_model_url (str): The B-UML domain model URL location.

        Returns:
            str: RDF vocabulary for the domain model, or an error message if generation fails.
        """
        # Get the model
        serialized_domain_model = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(serialized_domain_model)
        out = base_rdf_generation(domain_model)
        if out is not None:
            return out
        try:
            with open("./vocabulary.ttl", "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            content = "\n".join(lines)
            os.remove("./vocabulary.ttl")
            return content

        except Exception as e:
            # Try to provide more detailed information about why no RDF was generated
            classes = domain_model.get_classes()
            classes_info = []
            for cls in classes:
                attr_count = len(cls.attributes)
                classes_info.append(f"{cls.name} ({attr_count} attributes)")

            if not classes:
                return "No RDF vocabulary generated. The domain model contains no classes."
            else:
                return f"No RDF vocabulary generated. The domain model contains {len(classes)} class(es): {', '.join(classes_info)}. The RDF vocabulary generator may require additional configuration or the classes may not meet generation requirements."


def register_generator_tools(mcp, logger):
    @mcp.tool()
    def sql_generation(sql_dialect: str = "sqlite", output_dir: str = "."):
        """Creates a SQL representation of the model.

        Args:
            sql_dialect (str) : The SQL dialect of the output (default sqlite).
            output_dir (str): Absolute path of the output directory for generating files
        """
        # Get the model
        domain_model = get_model()
        out = base_sql_generation(domain_model, sql_dialect, path=output_dir)
        return "Success" if out is None else out


    @mcp.tool()
    def python_generation(output_dir: str = "."):
        """Creates a set of python classes implementing the model.

        Args:
            output_dir (str): Absolute path of the output directory for generating files
        """
        # Get the model
        domain_model = get_model()
        out = base_python_generation(domain_model, output_dir)
        return "Success" if out is None else out

    @mcp.tool()
    def backend_generation(output_dir: str = "."):
        """Generate a backend to store and manipulate model instances.

        Args:
            output_dir (str): Absolute path of the output directory for generating files
        """
        # Get the model
        domain_model = get_model()
        out = base_backend_generation(domain_model, output_dir)
        return "Success" if out is None else out


    @mcp.tool()
    def java_generation(output_dir: str = "."):
        """Creates a set of Java classes implementing the model.

        Args:
            output_dir (str): Absolute path of the output directory for generating files
        """
        # Get the model
        domain_model = get_model()
        out = base_java_generation(domain_model, output_dir)
        return "Success" if out is None else out


    @mcp.tool()
    def json_schema_generation(output_dir: str = "."):
        """Creates a JSON schema for the model.

        Args:
            output_dir (str): Absolute path of the output directory for generating files
        """
        # Get the model
        domain_model = get_model()
        out = base_json_generation(domain_model, output_dir)
        return "Success" if out is None else out

    @mcp.tool()
    def json_smart_data_generation(output_dir: str = "."):
        """Creates a JSON smart data schema for the model.

        Args:
            output_dir (str): Absolute path of the output directory for generating files
        """
        # Get the model
        domain_model = get_model()
        out = base_json_generation(domain_model, output_dir, mode="smart_data")
        return "Success" if out is None else out

    @mcp.tool()
    def pydantic_classes_generation(output_dir: str = "."):
        """Creates a Pydentic implementation of the model.

        Args:
            output_dir (str): Absolute path of the output directory for generating files
        """
        # Get the model
        domain_model = get_model()
        out = base_pydantic_classes_generation(domain_model, output_dir)
        return "Success" if out is None else out


    @mcp.tool()
    def rdf_generation(output_dir: str = "."):
        """Generates the RDF vocabulary for the model.

        Args:
            output_dir (str): Absolute path of the output directory for generating files
        """
        # Get the model
        domain_model = get_model()
        out = base_rdf_generation(domain_model, output_dir)
        return "Success" if out is None else out


    @mcp.tool()
    def rest_api_generation(output_dir: str = "."):
        """Generate the Rest API domain model code.

        Args:
            output_dir (str): Absolute path of the output directory for generating files
        """
        # Get the model
        domain_model = get_model()
        out = base_rest_api_generation(domain_model, output_dir)
        return "Success" if out is None else out


    @mcp.tool()
    def sql_alchemy_generation(output_dir: str = "."):
        """Generate the SQLAlchemy code for the model.

        Args:
            output_dir (str): Absolute path of the output directory for generating files
        """
        # Get the model
        domain_model = get_model()
        out = base_sql_alchemy_generation(domain_model, output_dir)
        return "Success" if out is None else out


