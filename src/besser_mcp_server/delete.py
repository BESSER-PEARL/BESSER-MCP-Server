from src.besser_mcp_server.utils import multiplicity_from_string, serialize_domain_model, deserialize_domain_model


def register_deletion_tools(mcp, logger):

    @mcp.tool()
    async def delete_class(
            domain_model_base64: str,
            name: str,
    ) -> str:
        """Remove a `Class` instance from a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): Name of the class.

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        try:
            logger.info(f"Removing class '{name}' to domain model")
            # Deserialize the domain model
            domain_model = deserialize_domain_model(domain_model_base64)

            to_remove = domain_model.get_type_by_name(name)

            if to_remove is None:
                logger.warning(f"Class '{name}' do not exists in model")
                return f"Error removing class '{name}': No class with name '{name}' exists in the model"
            else:
                domain_model.type.remove(to_remove)

            # Return the updated model as base64
            return serialize_domain_model(domain_model)

        except ValueError as e:
            # Return error message if class with same name already exists
            return f"Error removing class '{name}': {str(e)}"
        except Exception as e:
            return f"Error processing domain model: {str(e)}"


    @mcp.tool()
    async def delete_method_from_class(
            domain_model_base64: str,
            name: str,
            class_name: str
    ) -> str:
        """Removes a new method from a `Class` instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the method.
            class_name (str): The name of the class that will contain the method.

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        try:
            logger.info(f"Removing method '{name}' from class '{class_name}'")
            # Deserialize the domain model
            domain_model = deserialize_domain_model(domain_model_base64)

            the_class = domain_model.get_type_by_name(class_name)
            the_method = None
            for method in the_class.methods:
                if method.name == name:
                    the_method = method
                    break

            if the_method is None:
                logger.warning(f"Method '{name}' do not exists in '{class_name}'")
                return f"Error removing method '{name}': No method with name '{name}' exists in '{class_name}'"
            else:
                the_class.methods.remove(the_method)
            logger.info(f"Successfully removed method '{name}' from class '{class_name}'")

            # Return the updated model as base64
            return serialize_domain_model(domain_model)

        except ValueError as e:
            # Return error message if class with same name already exists
            return f"Error removing method '{name}' from class '{class_name}': {str(e)}"
        except Exception as e:
            return f"Error processing domain model: {str(e)}"


    @mcp.tool()
    async def delete_attribute_from_class(
            domain_model_base64: str,
            name: str,
            class_name: str
    ) -> str:
        """Adds a new attribute to a `Class` instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the property.
            class_name (str): The name of the class that will contain the attribute.

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        try:
            logger.info(f"Removing attribute '{name}' from class '{class_name}'")
            # Deserialize the domain model
            domain_model = deserialize_domain_model(domain_model_base64)

            the_class = domain_model.get_type_by_name(class_name)
            the_attribute = None
            for attribute in the_class.attributes:
                if attribute.name == name:
                    the_attribute = attribute
                    break

            if the_attribute is None:
                logger.warning(f"Attribute '{name}' do not exists in '{class_name}'")
                return f"Error removing attribute '{name}': No attribute with name '{name}' exists in '{class_name}'"
            else:
                the_class.attributes.remove(the_attribute)
            logger.info(f"Successfully removed attribute '{name}' from class '{class_name}'")

            # Return the updated model as base64
            return serialize_domain_model(domain_model)

        except ValueError as e:
            # Return error message if class with same name already exists
            return f"Error removing attribute '{name}' from class '{class_name}': {str(e)}"
        except Exception as e:
            return f"Error processing domain model: {str(e)}"




    @mcp.tool()
    async def delete_binary_association(
            domain_model_base64: str,
            name: str
    ) -> str:
        """Removes a BinaryAssociation instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the method.

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        try:
            logger.info(f"Removing association '{name}' from model")
            # Deserialize the domain model
            domain_model = deserialize_domain_model(domain_model_base64)

            the_association = None
            for association in domain_model.associations:
                if association.name == name:
                    the_association = association

            if the_association is None:
                logger.warning(f"Association '{name}' do not exists in model")
                return f"Error removing association '{name}': No association with name '{name}' exists in model"
            else:
                domain_model.associations.remove(the_association)

            logger.info(f"Successfully removed association '{name}' from model")

            # Return the updated model as base64
            return serialize_domain_model(domain_model)

        except ValueError as e:
            return f"Error removing association '{name}' to model: {str(e)}"
        except Exception as e:
            return f"Error processing domain model: {str(e)}"



    @mcp.tool()
    async def delete_association_class(
            domain_model_base64: str,
            name: str
    ) -> str:
        """Removes an association class in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the association class.

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        try:
            logger.info(f"Removing association class '{name}' to domain model")
            # Deserialize the domain model
            domain_model = deserialize_domain_model(domain_model_base64)

            to_remove = domain_model.get_type_by_name(name)

            if to_remove is None:
                logger.warning(f"AssociationClass '{name}' do not exists in model")
                return f"Error removing association class '{name}': No association class with name '{name}' exists in the model"
            else:
                domain_model.type.remove(to_remove)

            # Return the updated model as base64
            return serialize_domain_model(domain_model)

        except ValueError as e:
            # Return error message if class with same name already exists
            return f"Error removing association class '{name}': {str(e)}"
        except Exception as e:
            return f"Error processing domain model: {str(e)}"



    @mcp.tool()
    async def delete_enumeration(
            domain_model_base64: str,
            name: str
    ) -> str:
        """Removes an Enumeration instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the enumeration.

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        try:
            logger.info(f"Removing Enumeration '{name}' to domain model")
            # Deserialize the domain model
            domain_model = deserialize_domain_model(domain_model_base64)

            to_remove = domain_model.get_type_by_name(name)

            if to_remove is None:
                logger.warning(f"Enumeration '{name}' do not exists in model")
                return f"Error removing enumeration '{name}': No enumeration with name '{name}' exists in the model"
            else:
                domain_model.type.remove(to_remove)

            # Return the updated model as base64
            return serialize_domain_model(domain_model)

        except ValueError as e:
            # Return error message if class with same name already exists
            return f"Error removing enumeration '{name}': {str(e)}"
        except Exception as e:
            return f"Error processing domain model: {str(e)}"



    @mcp.tool()
    async def delete_enumeration_literal(
            domain_model_base64: str,
            name: str,
            enumeration_name: str
    ) -> str:
        """Removes a literal from an `Enumeration` instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            name (str): The name of the method.
            enumeration_name (str): The name of the enumeration that will contain the literal.

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        try:
            logger.info(f"Removing literal '{name}' from enumeration '{enumeration_name}'")
            # Deserialize the domain model
            domain_model = deserialize_domain_model(domain_model_base64)

            the_enumeration = domain_model.get_type_by_name(enumeration_name)
            the_literal = None
            for literal in the_enumeration.literals:
                if literal.name == name:
                    the_literal = literal
                    break

            if the_literal is None:
                logger.warning(f"Literal '{name}' do not exists in '{enumeration_name}'")
                return f"Error removing literal '{name}': No literal with name '{name}' exists in '{enumeration_name}'"
            else:
                the_enumeration.literals.remove(the_literal)
            logger.info(f"Successfully removed literal '{name}' from enumeration '{enumeration_name}'")

            # Return the updated model as base64
            return serialize_domain_model(domain_model)

        except ValueError as e:
            # Return error message if enumeration with same name already exists
            return f"Error removing method '{name}' from enumeration '{enumeration_name}': {str(e)}"
        except Exception as e:
            return f"Error processing domain model: {str(e)}"



    @mcp.tool()
    async def delete_generalization(
            domain_model_base64: str,
            general_class_name: str,
            specific_class_name: str
    ) -> str:
        """Removes a Generalization instance in a B-UML DomainModel and returns the updated model as base64.

        Args:
            domain_model_base64 (str): The B-UML domain model as base64 string.
            general_class_name (str): Class name of the general class
            specific_class_name (str): Class name of the specific class

        Returns:
            str: The updated domain model as base64 string, or an error message
                 if a class with the same name already exists.
        """
        try:
            logger.info(f"Removing generalization '{general_class_name}' <|-- '{specific_class_name}' from model")
            # Deserialize the domain model
            domain_model = deserialize_domain_model(domain_model_base64)

            general_class = domain_model.get_type_by_name(general_class_name)
            specific_class = domain_model.get_type_by_name(specific_class_name)

            the_generalization = None
            for generalization in domain_model.generalizations:
                if generalization.general == general_class and generalization.specific == specific_class:
                    the_generalization = generalization

            if the_generalization is None:
                logger.warning(f"Generalization '{general_class_name}' <|-- '{specific_class_name}' do not exists in model")
                return f"Error removing genralization '{general_class_name}' <|-- '{specific_class_name}': No generalization between '{general_class_name}' and '{specific_class_name}' exists in model'"
            else:
                general_class.generalizations.remove(the_generalization)
                specific_class.generalizations.remove(the_generalization)
                domain_model.generalizations.remove(the_generalization)

            logger.info(f"Successfully removed generalization '{general_class_name}' <|-- '{specific_class_name}' from model")

            # Return the updated model as base64
            return serialize_domain_model(domain_model)

        except ValueError as e:
            return f"Error removing generalization '{general_class_name}' <|-- '{specific_class_name}' to model: {str(e)}"
        except Exception as e:
            return f"Error processing domain model: {str(e)}"