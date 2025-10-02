import base64
import pickle

from besser.BUML.metamodel.structural import Multiplicity

from src.besser_mcp_server.server import logger

serialization = ""

def serialize_domain_model(domain_model) -> str:
    """Convert a domain model to a base64 string using pickle."""
    global serialization
    try:

        # Serialize the domain model using pickle
        pickled_data = pickle.dumps(domain_model)

        # Convert to base64 for string representation
        encoded_data = base64.b64encode(pickled_data).decode('ascii')
        serialization = encoded_data

        return encoded_data

    except Exception as e:
        logger.error(f"Error serializing model: {str(e)}")
        return f"Error serializing model: {str(e)}"


def deserialize_domain_model(model_base64: str):
    """Convert a base64 string back to a domain model object using pickle."""
    global serialization
    try:
        if serialization != model_base64:
            logger.error(f"Serialization mismatch: The model may be truncated")
        # Decode from base64
        pickled_data = base64.b64decode(model_base64.encode('ascii') + b'==')  # adding "==" avoid padding problems

        # Deserialize using pickle
        domain_model = pickle.loads(pickled_data)

        return domain_model

    except Exception as e:
        raise RuntimeError(f"Error deserializing model: {str(e)}")

def multiplicity_from_string(multiplicity_str):
    bounds = multiplicity_str.split("..")
    if len(bounds) != 2:
        raise ValueError(f"Multiplicity string '{multiplicity_str}' must have min and max values")
    min = int(bounds[0])
    max = bounds[1]
    if bounds[1] != "*":
        max = int(bounds[1])
    return Multiplicity(min, max)