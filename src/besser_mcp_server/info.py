from besser.BUML.metamodel.structural import DomainModel
from utils import deserialize_domain_model, download_model_from, get_model


def base_about() -> str:
    """Get information about BESSER and this MCP server."""
    return (
        "BESSER is a Python-based low-modeling low-code platform for smart and AI-enhanced software development. "
        "It provides modeling capabilities and code generation tools to help developers build software faster.\n\n"
        "Learn more about BESSER at: https://github.com/BESSER-PEARL/BESSER")

def base_get_model_info(logger, domain_model: DomainModel) -> str:
    """Get detailed information about a domain model.

    Args:
        domain_model (DomainModel): The B-UML domain model.

    Returns:
        str: Detailed information about the domain model.
    """
    try:
        logger.info("Getting model info")
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

def register_base64_info_tools(mcp, logger):
    @mcp.tool()
    def about() -> str:
        """Get information about BESSER and this MCP server."""
        return base_about()

    @mcp.tool()
    def get_base64_model_info(domain_model_base64: str) -> str:
        """Get detailed information about a domain model.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.

        Returns:
            str: Detailed information about the domain model.
        """
        domain_model = deserialize_domain_model(domain_model_base64)
        return base_get_model_info(logger, domain_model)

def register_url_info_tools(mcp, logger):
    @mcp.tool()
    def about() -> str:
        """Get information about BESSER and this MCP server."""
        return base_about()

    @mcp.tool()
    def get_model_info_with_url(domain_model_url: str) -> str:
        """Get detailed information about a domain model.

        Args:
            domain_model_url (str): The B-UML domain model URL location.

        Returns:
            str: Detailed information about the domain model.
        """
        # Get the model
        serialized_domain_model = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(serialized_domain_model)
        return base_get_model_info(logger, domain_model)

def register_info_tools(mcp, logger):
    @mcp.tool()
    def about() -> str:
        """Get information about BESSER and this MCP server."""
        return base_about()

    @mcp.tool()
    def get_model_info() -> str:
        """Get detailed information about a domain model.

        Returns:
            str: Detailed information about the domain model.
        """
        # Get the model
        domain_model = get_model()
        return base_get_model_info(logger, domain_model)