from besser.BUML.metamodel.structural import DomainModel
from utils import (multiplicity_from_string, serialize_domain_model, deserialize_domain_model,
                                         download_model_from, upload_model_to, save_model, get_model)


def base_add_class(
        logger,
        domain_model: DomainModel,
        name: str,
        attributes=None,
        methods=None,
        is_abstract: bool = False,
        is_read_only: bool = False,
        behaviors=None,
        timestamp=None,
        metadata=None,
        is_derived: bool = False,
) -> DomainModel | str:
    """Adds a new `Class` instance to a B-UML DomainModel.

    Args:
        domain_model (DomainModel): The B-UML domain model.
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

        # Return the updated model
        return domain_model

    except ValueError as e:
        # Return error message if class with same name already exists
        return f"Error adding class '{name}': {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"


def base_add_method_to_class(
        logger,
        domain_model: DomainModel,
        name: str,
        class_name: str,
        visibility: str = "public",
        is_abstract: bool = False,
        parameters: dict[str ,str] = dict(),
        type_name :str = "str",
        code: str = "",
        timestamp = None,
        metadata = None,
        is_derived: bool = False
) -> DomainModel | str:
    """Adds a new method to a `Class` instance in a B-UML DomainModel.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        name (str): The name of the method.
        class_name (str): The name of the class that will contain the method.
        visibility (str): Determines the kind of visibility of the method (public as default).
        is_abstract (bool): Indicates if the method is abstract (False as default).
        parameters (dict[str,str]): The mapping of parameters name and type for the method (dict() as default).
        type_name (str): The name of the type of the method ("str" as default).
        code (str): code of the method ("" as default).
        timestamp (datetime | None): Object creation datetime (default is current time).
        metadata (Metadata | None): Metadata information for the method (None as default).
        is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

    Returns:
        str: The updated domain model as base64 string, or an error message
             if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import Parameter, Method  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    try:
        logger.info(f"Adding method '{name}' to class '{class_name}'")

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)


        owner = domain_model.get_type_by_name(class_name)
        existing_methods = owner.methods
        existing_method_names = {method.name for method in existing_methods}

        method_type = domain_model.get_type_by_name(type_name)

        if name in existing_method_names:
            logger.warning(f"Method '{name}' already exists in Class '{class_name}'")
            return f"Error adding method '{name}': A method with name '{name}' already exists in the class '{class_name}'"

        parameter_objects = set()
        for param_name, param_type_name in parameters.items():
            param_type = domain_model.get_type_by_name(type_name)
            parameter_objects.add(Parameter(param_name, param_type))

        new_method = Method(
            name,
            visibility,
            is_abstract,
            parameter_objects,
            method_type,
            owner,
            code,
            timestamp,  # type: ignore[arg-type]
            metadata,
            is_derived
        )

        owner.add_method(new_method)
        logger.info(f"Successfully added method '{name}' to class '{class_name}'")

        # Return the updated model
        return domain_model

    except ValueError as e:
        # Return error message if class with same name already exists
        return f"Error adding method '{name}' to class '{class_name}': {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"


def base_add_attribute_to_class(
        logger,
        domain_model: DomainModel,
        name: str,
        class_name: str,
        type_name :str = None,
        multiplicity_str = "1..1",
        visibility :str = "public",
        is_composite :bool = False,
        is_navigable :bool = True,
        is_id :bool = False,
        is_read_only :bool = False,
        timestamp = None,
        metadata = None,
        is_derived :bool = False,
) -> DomainModel | str:
    """Adds a new attribute to a `Class` instance in a B-UML DomainModel.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        name (str): The name of the property.
        class_name (str): The name of the class that will contain the attribute.
        type_name (str): The type of the property.
        multiplicity_str (str): The multiplicity of the property (1..1 as default).
        visibility (str): The visibility of the property (public as default).
        is_composite (bool): Indicates whether the property is a composite (False as default).
        is_navigable (bool): Indicates whether the property is navigable in a relationship (True as default).
        is_id (bool): Indicates whether the property is an id (False as default).
        is_read_only (bool): Indicates whether the property is read only (False as default).
        timestamp (datetime | None): Object creation datetime (default is current time).
        metadata (Metadata | None): Metadata information for the property (None as default).
        is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

    Returns:
        str: The updated domain model as base64 string, or an error message
             if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import Multiplicity, Property  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    try:
        logger.info(f"Adding attribute '{name}' to class '{class_name}'")

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        owner = domain_model.get_type_by_name(class_name)
        existing_attributes = owner.attributes
        existing_attribute_names = {attribute.name for attribute in existing_attributes}

        property_type = domain_model.get_type_by_name(type_name)

        if name in existing_attribute_names:
            logger.warning(f"Attribute '{name}' already exists in Class '{class_name}'")
            return f"Error adding attribute '{name}': An attribute with name '{name}' already exists in the class '{class_name}'"

        multiplicity = multiplicity_from_string(multiplicity_str)

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

        # Return the updated model
        return domain_model

    except ValueError as e:
        # Return error message if class with same name already exists
        return f"Error adding attribute '{name}' to class '{class_name}': {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"




def base_add_binary_association(
        logger,
        domain_model: DomainModel,
        name: str,
        from_class: str,
        to_class: str,
        role_from: str,
        role_to: str,
        multiplicity_from: str = "1..1",
        multiplicity_to: str = "1..1",
        is_bidirectional: bool = True,
        is_composition: bool = False,
        timestamp = None,
        metadata = None,
        is_derived: bool = False,
) -> DomainModel | str:
    """Adds a new BinaryAssociation instance in a B-UML DomainModel.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        name (str): The name of the method.
        from_class (str): Class name of the 'from' end of the association
        to_class (str): Class name of the 'to' end of the association
        role_from (str): Name/Role of the 'from' end of the association
        role_to (str): Name/Role of the 'to' end of the association
        multiplicity_from (str): Multiplicity of the 'from' end of the association ('1..1' as default)
        multiplicity_to (str): Multiplicity of the 'to' end of the association ('1..1' as default)
        is_bidirectional (bool): indicates whether the association is bidirectional (True as default).
        is_composition (bool): Indicates whether the association is a composition (False as default).
        timestamp (datetime | None): Object creation datetime (default is current time).
        metadata (Metadata | None): Metadata information for the property (None as default).
        is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

    Returns:
        str: The updated domain model as base64 string, or an error message
             if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import Property, BinaryAssociation  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    try:
        logger.info(f"Adding association '{name}' to model")

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)


        from_end_class = domain_model.get_type_by_name(from_class)
        to_end_class = domain_model.get_type_by_name(to_class)

        existing_association_names = {x.name for x in domain_model.associations}
        if name in existing_association_names:
            logger.warning(f"Association '{name}' already exists in the model")
            return f"Error adding association '{name}': An association with name '{name}' already exists in the model"

        try:
            multiplicity_to_obj = multiplicity_from_string(multiplicity_to)
        except ValueError as e:
            return f"Error adding association '{name}' to model: {str(e)}"
        try:
            multiplicity_from_obj = multiplicity_from_string(multiplicity_from)
        except ValueError as e:
            return f"Error adding association '{name}' to model: {str(e)}"


        from_end = Property(
            role_to,
            to_end_class,
            from_end_class,
            multiplicity_to_obj,
            is_composite = is_composition,
            timestamp = timestamp, # type: ignore[arg-type]
            metadata = metadata,
            is_derived = is_derived,
        )

        to_end = Property(
            role_from,
            from_end_class,
            to_end_class,
            multiplicity_from_obj,
            is_navigable=is_bidirectional,
            timestamp=timestamp,  # type: ignore[arg-type]
            metadata=metadata,
            is_derived=is_derived,
        )

        association = BinaryAssociation(name, {from_end, to_end}, timestamp, metadata, is_derived)
        domain_model.add_association(association)
        logger.info(f"Successfully added association '{name}' to model")

        # Return the updated model
        return domain_model

    except ValueError as e:
        return f"Error adding association '{name}' to model: {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"



def base_add_association_class(
        logger,
        domain_model: DomainModel,
        name: str,
        association_name: str,
        timestamp = None,
        metadata = None,
        is_derived: bool = False
) -> DomainModel | str:
    """Adds a new method to a `Class` instance in a B-UML DomainModel.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        name (str): The name of the association class.
        association_name (str): The name of the underlying association existing in the model (association needs to exist).
        timestamp (datetime | None): Object creation datetime (default is current time).
        metadata (Metadata | None): Metadata information for the method (None as default).
        is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

    Returns:
        str: The updated domain model as base64 string, or an error message
             if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import AssociationClass  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    try:
        logger.info(f"Adding association class '{name}' to model")

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        the_association = None
        for association in domain_model.associations:
            if association_name == association.name:
                the_association = association
                break

        if the_association is None:
            logger.warning(f"Association '{association_name}' does not exists in the model. Create the '{association_name}' association before the association class")
            return f"Error adding association class '{name}': Association '{association_name}' does not exists in the model. Create the '{association_name}' association before the association class"

        associationclass = AssociationClass(name, None, the_association, timestamp, metadata, is_derived)
        domain_model.add_type(associationclass)
        logger.info(f"Successfully added association class '{name}' to model")

        # Return the updated model
        return domain_model

    except ValueError as e:
        return f"Error adding association class '{name}' to model: {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"



def base_add_enumeration(
        logger,
        domain_model: DomainModel,
        name: str,
        literals: set[str],
        timestamp = None,
        metadata = None
) -> DomainModel | str:
    """Adds a new Enumeration instance in a B-UML DomainModel.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        name (str): The name of the enumeration.
        literals (set[str]): List of the literals in the Enumeration.
        timestamp (datetime | None): Object creation datetime (default is current time).
        metadata (Metadata | None): Metadata information for the method (None as default).

    Returns:
        str: The updated domain model as base64 string, or an error message
             if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import Enumeration, EnumerationLiteral  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    try:
        logger.info(f"Adding enumeration '{name}' to model")

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        if domain_model.get_type_by_name(name) is not None:
            logger.warning(f"Type '{name}' already exists in model")
            return f"Error adding enumeration '{name}': A type with name '{name}' already exists in the model"

        enum = Enumeration(name, {EnumerationLiteral(name=given_name) for given_name in literals}, timestamp, metadata)

        domain_model.add_type(enum)
        logger.info(f"Successfully added enumeration '{name}' to model")

        # Return the updated model
        return domain_model

    except ValueError as e:
        # Return error message if class with same name already exists
        return f"Error adding enumeration '{name}' to model: {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"



def base_add_enumeration_literal(
        logger,
        domain_model: DomainModel,
        name: str,
        enumeration_name: str,
        timestamp = None,
        metadata = None
) -> DomainModel | str:
    """Adds a new literal to an `Enumeration` instance in a B-UML DomainModel.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        name (str): The name of the method.
        enumeration_name (str): The name of the enumeration that will contain the literal.
        timestamp (datetime | None): Object creation datetime (default is current time).
        metadata (Metadata | None): Metadata information for the method (None as default).

    Returns:
        str: The updated domain model as base64 string, or an error message
             if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import EnumerationLiteral  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    try:
        logger.info(f"Adding literal '{name}' to enumeration '{enumeration_name}'")

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        enum = domain_model.get_type_by_name(enumeration_name)

        literal = EnumerationLiteral(name=name, owner=enum, timestamp=timestamp, metadata=metadata)

        enum.add_literal(literal)
        logger.info(f"Successfully added literal '{name}' to enumeration '{enumeration_name}'")

        # Return the updated model
        return domain_model

    except ValueError as e:
        # Return error message if class with same name already exists
        return f"Error adding literal '{name}' to enumeration '{enumeration_name}': {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"



def base_add_generalization(
        logger,
        domain_model: DomainModel,
        general_class_name: str,
        specific_class_name: str,
        timestamp=None,
        is_derived: bool = False,
) -> DomainModel | str:
    """Adds a new Generalization instance in a B-UML DomainModel.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        general_class_name (str): Class name of the general class
        specific_class_name (str): Class name of the specific class
        timestamp (datetime | None): Object creation datetime (default is current time).
        is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

    Returns:
        str: The updated domain model as base64 string, or an error message
             if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import Generalization  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    try:
        logger.info(f"Adding generalization '{general_class_name}' <|-- '{specific_class_name}' to model")

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        general_class = domain_model.get_type_by_name(general_class_name)
        specific_class = domain_model.get_type_by_name(specific_class_name)

        generalization = Generalization(general=general_class, specific=specific_class, timestamp=timestamp, is_derived=is_derived)
        domain_model.add_generalization(generalization)
        logger.info(f"Successfully added generalization '{general_class_name}' <|-- '{specific_class_name}' to model")

        # Return the updated model
        return domain_model

    except ValueError as e:
        return f"Error adding association '{general_class_name}' <|-- '{specific_class_name}' to model: {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"



def base_add_ocl_constraint(
        logger,
        domain_model: DomainModel,
        name: str,
        class_name: str,
        expression: str,
        timestamp: int = None,
        is_derived: bool = False,
) -> DomainModel | str:
    """Adds a new Package instance in a B-UML DomainModel.

    Args:
        domain_model (DomainModel): The B-UML domain model.
        name (str): name of the constraint
        class_name (str): Class name of the general class
        expression (str): the OCL expression
        timestamp (datetime | None): Object creation datetime (default is current time).
        is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

    Returns:
        str: The updated domain model as base64 string, or an error message
             if a class with the same name already exists.
    """
    from datetime import datetime
    from datetime import timezone

    try:
        from besser.BUML.metamodel.structural import Constraint  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BESSER library must be installed (`pip install besser`)."
        ) from exc

    try:
        logger.info(f"Adding constraint '{name}' to class {class_name}")

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        context = domain_model.get_type_by_name(class_name)
        constraint = Constraint(name, context, expression, "OCL", timestamp, is_derived=is_derived)

        domain_model.constraints = domain_model.constraints.union({constraint})
        logger.info(f"Successfully added constraint '{name}' to class {class_name}")

        # Return the updated model
        return domain_model

    except ValueError as e:
        return f"Error adding constraint '{name}' to class {class_name}: {str(e)}"
    except Exception as e:
        return f"Error processing domain model: {str(e)}"


def register_base64_creation_tools(mcp, logger):

    @mcp.tool()
    def new_model_base64(name: str) -> str:
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
    def add_class_base64(
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
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_class(logger, domain_model, name, attributes, methods, is_abstract, is_read_only, behaviors, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        # Return the updated model as base64
        return serialize_domain_model(domain_model)


    @mcp.tool()
    def add_method_to_class_base64(
            domain_model_base64: str,
            name: str,
            class_name: str,
            visibility: str = "public",
            is_abstract: bool = False,
            parameters: dict[str ,str] = dict(),
            type_name :str = "str",
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
            parameters (dict[str,str]): The mapping of parameters name and type for the method (dict() as default).
            type_name (str): The name of the type of the method ("str" as default).
            code (str): code of the method ("" as default).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_method_to_class(logger,domain_model, name, class_name, visibility, is_abstract, parameters, type_name, code, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        # Return the updated model as base64
        return serialize_domain_model(domain_model)


    @mcp.tool()
    def add_attribute_to_class_base64(
            domain_model_base64: str,
            name: str,
            class_name: str,
            type_name :str = None,
            multiplicity_str = "1..1",
            visibility :str = "public",
            is_composite :bool = False,
            is_navigable :bool = True,
            is_id :bool = False,
            is_read_only :bool = False,
            timestamp = None,
            metadata = None,
            is_derived :bool = False,
    ) -> str:
        """Adds a new attribute to a `Class` instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the property.
            class_name (str): The name of the class that will contain the attribute.
            type_name (str): The type of the property.
            multiplicity_str (str): The multiplicity of the property (1..1 as default).
            visibility (str): The visibility of the property (public as default).
            is_composite (bool): Indicates whether the property is a composite (False as default).
            is_navigable (bool): Indicates whether the property is navigable in a relationship (True as default).
            is_id (bool): Indicates whether the property is an id (False as default).
            is_read_only (bool): Indicates whether the property is read only (False as default).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the property (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_attribute_to_class(logger, domain_model, name, class_name, type_name, multiplicity_str, visibility, is_composite, is_navigable, is_id, is_read_only, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        # Return the updated model as base64
        return serialize_domain_model(domain_model)




    @mcp.tool()
    def add_binary_association_base64(
            domain_model_base64: str,
            name: str,
            from_class: str,
            to_class: str,
            role_from: str,
            role_to: str,
            multiplicity_from: str = "1..1",
            multiplicity_to: str = "1..1",
            is_bidirectional: bool = True,
            is_composition: bool = False,
            timestamp = None,
            metadata = None,
            is_derived: bool = False,
    ) -> str:
        """Adds a new BinaryAssociation instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the method.
            from_class (str): Class name of the 'from' end of the association
            to_class (str): Class name of the 'to' end of the association
            role_from (str): Name/Role of the 'from' end of the association
            role_to (str): Name/Role of the 'to' end of the association
            multiplicity_from (str): Multiplicity of the 'from' end of the association ('1..1' as default)
            multiplicity_to (str): Multiplicity of the 'to' end of the association ('1..1' as default)
            is_bidirectional (bool): indicates whether the association is bidirectional (True as default).
            is_composition (bool): Indicates whether the association is a composition (False as default).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the property (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_binary_association(logger, domain_model, name, from_class, to_class, role_from, role_to, multiplicity_from, multiplicity_to, is_bidirectional, is_composition, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        # Return the updated model as base64
        return serialize_domain_model(domain_model)



    @mcp.tool()
    def add_association_class_base64(
            domain_model_base64: str,
            name: str,
            association_name: str,
            timestamp = None,
            metadata = None,
            is_derived: bool = False
    ) -> str:
        """Adds a new method to a `Class` instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the association class.
            association_name (str): The name of the underlying association existing in the model (association needs to exist).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_association_class(logger, domain_model, name, association_name, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        # Return the updated model as base64
        return serialize_domain_model(domain_model)



    @mcp.tool()
    def add_enumeration_base64(
            domain_model_base64: str,
            name: str,
            literals: set[str],
            timestamp = None,
            metadata = None
    ) -> str:
        """Adds a new Enumeration instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the enumeration.
            literals (set[str]): List of the literals in the Enumeration.
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_enumeration(logger, domain_model, name, literals, timestamp, metadata)
        if isinstance(domain_model, str):
            return domain_model

        # Return the updated model as base64
        return serialize_domain_model(domain_model)



    @mcp.tool()
    def add_enumeration_literal_base64(
            domain_model_base64: str,
            name: str,
            enumeration_name: str,
            timestamp = None,
            metadata = None
    ) -> str:
        """Adds a new literal to an `Enumeration` instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the method.
            enumeration_name (str): The name of the enumeration that will contain the literal.
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_enumeration_literal(logger, domain_model, name, enumeration_name, timestamp, metadata)
        if isinstance(domain_model, str):
            return domain_model

        # Return the updated model as base64
        return serialize_domain_model(domain_model)



    @mcp.tool()
    def add_ocl_constraint_base64(
            domain_model_base64: str,
            name: str,
            class_name: str,
            expression: str,
            timestamp=None,
            is_derived: bool = False,
    ) -> str:
        """Adds a new OCL constraint to a class in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): Name of the constraint
            class_name (str): Name of the class constrained
            expression (str): OCL expression of the constraint
            timestamp (datetime | None): Object creation datetime (default is current time).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: The updated domain model as base64 string, or an error message.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_ocl_constraint(logger, domain_model, name, class_name, expression, timestamp, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        # Return the updated model as base64
        return serialize_domain_model(domain_model)

    @mcp.tool()
    def add_generalization_base64(
            domain_model_base64: str,
            general_class_name: str,
            specific_class_name: str,
            timestamp=None,
            is_derived: bool = False,
    ) -> str:
        """Adds a new Generalization instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            general_class_name (str): Class name of the general class
            specific_class_name (str): Class name of the specific class
            timestamp (datetime | None): Object creation datetime (default is current time).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_generalization(logger, domain_model, general_class_name, specific_class_name, timestamp,
                                               is_derived)
        if isinstance(domain_model, str):
            return domain_model

        # Return the updated model as base64
        return serialize_domain_model(domain_model)


def register_url_creation_tools(mcp, logger):

    @mcp.tool()
    def new_model_with_url(domain_model_url: str, name: str) -> str:
        """Creates a new B-UML DomainModel with the specified name.

        Args:
            domain_model_url (str): location to save the model.
            name (str): Name of the new domain model.

        Returns:
            str: 'Success' or an error message.
        """
        try:
            from besser.BUML.metamodel.structural import DomainModel  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "BESSER library must be installed (`pip install besser`)."
            ) from exc

        # Create and return a new DomainModel instance as base64
        domain_model = DomainModel(name=name)
        serialized_model = serialize_domain_model(domain_model)
        # Upload the model
        upload_model_to(serialized_model, domain_model_url)
        return "Success"


    @mcp.tool()
    def add_class_with_url(
            domain_model_url: str,
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
        """Adds a new `Class` instance to a B-UML DomainModel.

        Args:
            domain_model_url (str): The B-UML domain model URL location.
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
            str: 'Success' or an error message
        """
        # Get the model from url
        domain_model_base64 = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_class(logger, domain_model, name, attributes, methods, is_abstract, is_read_only, behaviors, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        serialized_model = serialize_domain_model(domain_model)
        # Upload the model
        upload_model_to(serialized_model, domain_model_url)
        return "Success"


    @mcp.tool()
    def add_method_to_class_with_url(
            domain_model_url: str,
            name: str,
            class_name: str,
            visibility: str = "public",
            is_abstract: bool = False,
            parameters: dict[str ,str] = dict(),
            type_name :str = "str",
            code: str = "",
            timestamp = None,
            metadata = None,
            is_derived: bool = False
    ) -> str:
        """Adds a new method to a `Class` instance in a B-UML DomainModel.

        Args:
            domain_model_url (str): The B-UML domain model URL location.
            name (str): The name of the method.
            class_name (str): The name of the class that will contain the method.
            visibility (str): Determines the kind of visibility of the method (public as default).
            is_abstract (bool): Indicates if the method is abstract (False as default).
            parameters (dict[str,str]): The mapping of parameters name and type for the method (dict() as default).
            type_name (str): The name of the type of the method ("str" as default).
            code (str): code of the method ("" as default).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        # Get the model from url
        domain_model_base64 = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_method_to_class(logger, domain_model, name, class_name, visibility, is_abstract, parameters, type_name, code, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        serialized_model = serialize_domain_model(domain_model)
        # Upload the model
        upload_model_to(serialized_model, domain_model_url)
        return "Success"


    @mcp.tool()
    def add_attribute_to_class_with_url(
            domain_model_url: str,
            name: str,
            class_name: str,
            type_name :str = None,
            multiplicity_str = "1..1",
            visibility :str = "public",
            is_composite :bool = False,
            is_navigable :bool = True,
            is_id :bool = False,
            is_read_only :bool = False,
            timestamp = None,
            metadata = None,
            is_derived :bool = False,
    ) -> str:
        """Adds a new attribute to a `Class` instance in a B-UML DomainModel.

        Args:
            domain_model_url (str): The B-UML domain model URL location.
            name (str): The name of the property.
            class_name (str): The name of the class that will contain the attribute.
            type_name (str): The type of the property.
            multiplicity_str (str): The multiplicity of the property (1..1 as default).
            visibility (str): The visibility of the property (public as default).
            is_composite (bool): Indicates whether the property is a composite (False as default).
            is_navigable (bool): Indicates whether the property is navigable in a relationship (True as default).
            is_id (bool): Indicates whether the property is an id (False as default).
            is_read_only (bool): Indicates whether the property is read only (False as default).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the property (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        # Get the model from url
        domain_model_base64 = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_attribute_to_class(logger, domain_model, name, class_name, type_name, multiplicity_str, visibility, is_composite, is_navigable, is_id, is_read_only, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        serialized_model = serialize_domain_model(domain_model)
        # Upload the model
        upload_model_to(serialized_model, domain_model_url)
        return "Success"




    @mcp.tool()
    def add_binary_association_with_url(
            domain_model_url: str,
            name: str,
            from_class: str,
            to_class: str,
            role_from: str,
            role_to: str,
            multiplicity_from: str = "1..1",
            multiplicity_to: str = "1..1",
            is_bidirectional: bool = True,
            is_composition: bool = False,
            timestamp = None,
            metadata = None,
            is_derived: bool = False,
    ) -> str:
        """Adds a new BinaryAssociation instance in a B-UML DomainModel.

        Args:
            domain_model_url (str): The B-UML domain model URL location.
            name (str): The name of the method.
            from_class (str): Class name of the 'from' end of the association
            to_class (str): Class name of the 'to' end of the association
            role_from (str): Name/Role of the 'from' end of the association
            role_to (str): Name/Role of the 'to' end of the association
            multiplicity_from (str): Multiplicity of the 'from' end of the association ('1..1' as default)
            multiplicity_to (str): Multiplicity of the 'to' end of the association ('1..1' as default)
            is_bidirectional (bool): indicates whether the association is bidirectional (True as default).
            is_composition (bool): Indicates whether the association is a composition (False as default).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the property (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        # Get the model from url
        domain_model_base64 = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_binary_association(logger, domain_model, name, from_class, to_class, role_from, role_to, multiplicity_from, multiplicity_to, is_bidirectional, is_composition, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        serialized_model = serialize_domain_model(domain_model)
        # Upload the model
        upload_model_to(serialized_model, domain_model_url)
        return "Success"



    @mcp.tool()
    def add_association_class_with_url(
            domain_model_url: str,
            name: str,
            association_name: str,
            timestamp = None,
            metadata = None,
            is_derived: bool = False
    ) -> str:
        """Adds a new method to a `Class` instance in a B-UML DomainModel.

        Args:
            domain_model_url (str): The B-UML domain model URL location.
            name (str): The name of the association class.
            association_name (str): The name of the underlying association existing in the model (association needs to exist).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        # Get the model from url
        domain_model_base64 = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_association_class(logger, domain_model, name, association_name, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        serialized_model = serialize_domain_model(domain_model)
        # Upload the model
        upload_model_to(serialized_model, domain_model_url)
        return "Success"



    @mcp.tool()
    def add_enumeration_with_url(
            domain_model_url: str,
            name: str,
            literals: set[str],
            timestamp = None,
            metadata = None
    ) -> str:
        """Adds a new Enumeration instance in a B-UML DomainModel.

        Args:
            domain_model_url (str): The B-UML domain model URL location.
            name (str): The name of the enumeration.
            literals (set[str]): List of the literals in the Enumeration.
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).

        Returns:
            str: 'Success' or an error message
        """
        # Get the model from url
        domain_model_base64 = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_enumeration(logger, domain_model, name, literals, timestamp, metadata)
        if isinstance(domain_model, str):
            return domain_model

        serialized_model = serialize_domain_model(domain_model)
        # Upload the model
        upload_model_to(serialized_model, domain_model_url)
        return "Success"



    @mcp.tool()
    def add_enumeration_literal_with_url(
            domain_model_url: str,
            name: str,
            enumeration_name: str,
            timestamp = None,
            metadata = None
    ) -> str:
        """Adds a new literal to an `Enumeration` instance in a B-UML DomainModel.

        Args:
            domain_model_url (str): The B-UML domain model URL location.
            name (str): The name of the method.
            enumeration_name (str): The name of the enumeration that will contain the literal.
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).

        Returns:
            str: 'Success' or an error message
        """
        # Get the model from url
        domain_model_base64 = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_enumeration_literal(logger, domain_model, name, enumeration_name, timestamp, metadata)
        if isinstance(domain_model, str):
            return domain_model

        serialized_model = serialize_domain_model(domain_model)
        # Upload the model
        upload_model_to(serialized_model, domain_model_url)
        return "Success"



    @mcp.tool()
    def add_generalization_with_url(
            domain_model_url: str,
            general_class_name: str,
            specific_class_name: str,
            timestamp=None,
            is_derived: bool = False,
    ) -> str:
        """Adds a new Generalization instance in a B-UML DomainModel.

        Args:
            domain_model_url (str): The B-UML domain model URL location.
            general_class_name (str): Class name of the general class
            specific_class_name (str): Class name of the specific class
            timestamp (datetime | None): Object creation datetime (default is current time).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        # Get the model from url
        domain_model_base64 = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_generalization(logger, domain_model, general_class_name, specific_class_name, timestamp, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        serialized_model = serialize_domain_model(domain_model)
        # Upload the model
        upload_model_to(serialized_model, domain_model_url)
        return "Success"



    @mcp.tool()
    def add_ocl_constraint_with_url(
            domain_model_url: str,
            name: str,
            class_name: str,
            expression: str,
            timestamp=None,
            is_derived: bool = False,
    ) -> str:
        """Adds a new OCL constraint to a class in a B-UML DomainModel.

        Args:
            domain_model_url (str): The B-UML domain model URL location.
            name (str): Name of the constraint
            class_name (str): Name of the class constrained
            expression (str): OCL expression of the constraint
            timestamp (datetime | None): Object creation datetime (default is current time).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        # Get the model from url
        domain_model_base64 = download_model_from(domain_model_url)
        # Deserialize the domain model
        domain_model = deserialize_domain_model(domain_model_base64)

        domain_model = base_add_ocl_constraint(logger, domain_model, name, class_name, expression, timestamp,
                                               is_derived)
        if isinstance(domain_model, str):
            return domain_model

        serialized_model = serialize_domain_model(domain_model)
        # Upload the model
        upload_model_to(serialized_model, domain_model_url)
        return "Success"



def register_creation_tools(mcp, logger):

    @mcp.tool()
    def new_model(name: str) -> str:
        """Creates a new B-UML DomainModel with the specified name.

        Args:
            name (str): Name of the new domain model.

        Returns:
            str: 'Success' or an error message.
        """
        try:
            from besser.BUML.metamodel.structural import DomainModel  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "BESSER library must be installed (`pip install besser`)."
            ) from exc

        # Create and return a new DomainModel instance as base64
        domain_model = DomainModel(name=name)
        # Save the model
        save_model(domain_model)
        return "Success"


    @mcp.tool()
    def add_class(
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
        """Adds a new `Class` instance to a B-UML DomainModel.

        Args:
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
            str: 'Success' or an error message
        """
        domain_model = get_model()

        domain_model = base_add_class(logger, domain_model, name, attributes, methods, is_abstract, is_read_only, behaviors, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        save_model(domain_model)
        return "Success"


    @mcp.tool()
    def add_method_to_class(
            name: str,
            class_name: str,
            visibility: str = "public",
            is_abstract: bool = False,
            parameters: dict[str ,str] = dict(),
            type_name :str = "str",
            code: str = "",
            timestamp = None,
            metadata = None,
            is_derived: bool = False
    ) -> str:
        """Adds a new method to a `Class` instance in a B-UML DomainModel.

        Args:
            name (str): The name of the method.
            class_name (str): The name of the class that will contain the method.
            visibility (str): Determines the kind of visibility of the method (public as default).
            is_abstract (bool): Indicates if the method is abstract (False as default).
            parameters (dict[str,str]): The mapping of parameters name and type for the method (dict() as default).
            type_name (str): The name of the type of the method ("str" as default).
            code (str): code of the method ("" as default).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        domain_model = get_model()

        domain_model = base_add_method_to_class(logger, domain_model, name, class_name, visibility, is_abstract, parameters, type_name, code, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        save_model(domain_model)
        return "Success"


    @mcp.tool()
    def add_attribute_to_class(
            name: str,
            class_name: str,
            type_name :str = None,
            multiplicity_str = "1..1",
            visibility :str = "public",
            is_composite :bool = False,
            is_navigable :bool = True,
            is_id :bool = False,
            is_read_only :bool = False,
            timestamp = None,
            metadata = None,
            is_derived :bool = False,
    ) -> str:
        """Adds a new attribute to a `Class` instance in a B-UML DomainModel.

        Args:
            name (str): The name of the property.
            class_name (str): The name of the class that will contain the attribute.
            type_name (str): The type of the property.
            multiplicity_str (str): The multiplicity of the property (1..1 as default).
            visibility (str): The visibility of the property (public as default).
            is_composite (bool): Indicates whether the property is a composite (False as default).
            is_navigable (bool): Indicates whether the property is navigable in a relationship (True as default).
            is_id (bool): Indicates whether the property is an id (False as default).
            is_read_only (bool): Indicates whether the property is read only (False as default).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the property (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        domain_model = get_model()

        domain_model = base_add_attribute_to_class(logger, domain_model, name, class_name, type_name, multiplicity_str, visibility, is_composite, is_navigable, is_id, is_read_only, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        save_model(domain_model)
        return "Success"




    @mcp.tool()
    def add_binary_association(
            name: str,
            from_class: str,
            to_class: str,
            role_from: str,
            role_to: str,
            multiplicity_from: str = "1..1",
            multiplicity_to: str = "1..1",
            is_bidirectional: bool = True,
            is_composition: bool = False,
            timestamp = None,
            metadata = None,
            is_derived: bool = False,
    ) -> str:
        """Adds a new BinaryAssociation instance in a B-UML DomainModel.

        Args:
            name (str): The name of the method.
            from_class (str): Class name of the 'from' end of the association
            to_class (str): Class name of the 'to' end of the association
            role_from (str): Name/Role of the 'from' end of the association
            role_to (str): Name/Role of the 'to' end of the association
            multiplicity_from (str): Multiplicity of the 'from' end of the association ('1..1' as default)
            multiplicity_to (str): Multiplicity of the 'to' end of the association ('1..1' as default)
            is_bidirectional (bool): indicates whether the association is bidirectional (True as default).
            is_composition (bool): Indicates whether the association is a composition (False as default).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the property (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        domain_model = get_model()

        domain_model = base_add_binary_association(logger, domain_model, name, from_class, to_class, role_from, role_to, multiplicity_from, multiplicity_to, is_bidirectional, is_composition, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        save_model(domain_model)
        return "Success"



    @mcp.tool()
    def add_association_class(
            name: str,
            association_name: str,
            timestamp = None,
            metadata = None,
            is_derived: bool = False
    ) -> str:
        """Adds a new method to a `Class` instance in a B-UML DomainModel.

        Args:
            name (str): The name of the association class.
            association_name (str): The name of the underlying association existing in the model (association needs to exist).
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        domain_model = get_model()

        domain_model = base_add_association_class(logger, domain_model, name, association_name, timestamp, metadata, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        save_model(domain_model)
        return "Success"



    @mcp.tool()
    def add_enumeration(
            name: str,
            literals: set[str],
            timestamp = None,
            metadata = None
    ) -> str:
        """Adds a new Enumeration instance in a B-UML DomainModel.

        Args:
            name (str): The name of the enumeration.
            literals (set[str]): List of the literals in the Enumeration.
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).

        Returns:
            str: 'Success' or an error message
        """
        domain_model = get_model()

        domain_model = base_add_enumeration(logger, domain_model, name, literals, timestamp, metadata)
        if isinstance(domain_model, str):
            return domain_model

        save_model(domain_model)
        return "Success"



    @mcp.tool()
    def add_enumeration_literal(
            name: str,
            enumeration_name: str,
            timestamp = None,
            metadata = None
    ) -> str:
        """Adds a new literal to an `Enumeration` instance in a B-UML DomainModel.

        Args:
            name (str): The name of the method.
            enumeration_name (str): The name of the enumeration that will contain the literal.
            timestamp (datetime | None): Object creation datetime (default is current time).
            metadata (Metadata | None): Metadata information for the method (None as default).

        Returns:
            str: 'Success' or an error message
        """
        domain_model = get_model()

        domain_model = base_add_enumeration_literal(logger, domain_model, name, enumeration_name, timestamp, metadata)
        if isinstance(domain_model, str):
            return domain_model

        save_model(domain_model)
        return "Success"



    @mcp.tool()
    def add_generalization(
            general_class_name: str,
            specific_class_name: str,
            timestamp=None,
            is_derived: bool = False,
    ) -> str:
        """Adds a new Generalization instance in a B-UML DomainModel.

        Args:
            general_class_name (str): Class name of the general class
            specific_class_name (str): Class name of the specific class
            timestamp (datetime | None): Object creation datetime (default is current time).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        domain_model = get_model()

        domain_model = base_add_generalization(logger, domain_model, general_class_name, specific_class_name, timestamp, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        save_model(domain_model)
        return "Success"


    @mcp.tool()
    def add_ocl_constraint(
            name: str,
            class_name: str,
            expression: str,
            timestamp=None,
            is_derived: bool = False,
    ) -> str:
        """Adds a new OCL constraint to a class in a B-UML DomainModel.

        Args:
            name (str): Name of the constraint
            class_name (str): Name of the class constrained
            expression (str): OCL expression of the constraint
            timestamp (datetime | None): Object creation datetime (default is current time).
            is_derived (bool): Inherited from NamedElement, indicates whether the element is derived (False as default).

        Returns:
            str: 'Success' or an error message
        """
        # Get the model
        domain_model = get_model()

        domain_model = base_add_ocl_constraint(logger, domain_model, name, class_name, expression, timestamp, is_derived)
        if isinstance(domain_model, str):
            return domain_model

        save_model(domain_model)
        return "Success"