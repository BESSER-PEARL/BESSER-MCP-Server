import base64
import pickle

import requests

from besser.BUML.metamodel.structural import Multiplicity, DomainModel

from server import logger

domain_model = None

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

def upload_model_to(domain_model_base64: str, url: str):
    data = {'data': domain_model_base64}
    requests.post(url, json=data)

def download_model_from(url: str):
    body = requests.get(url)
    data = body.json()
    return data['data']

def get_model():
    global domain_model
    return domain_model

def save_model(model: DomainModel):
    global domain_model
    domain_model = model