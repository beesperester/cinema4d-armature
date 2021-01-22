from __future__ import annotations

import c4d

from fnmatch import fnmatch


class ValidationError(Exception):
    """
    This class represents a validation error
    """


class IValidator:

    def Validate(
        self,
        op: c4d.BaseObject
    ) -> bool:
        raise NotImplementedError(
            "Bound method 'Validate' must be implemented"
        )


class NameValidator(IValidator):

    def __init__(
        self,
        name_pattern: str
    ) -> None:
        self._name_pattern = name_pattern
    
    def Validate(
        self,
        op: c4d.BaseObject
    ) -> bool:
        """
        Validate the given name string against the name pattern
        using fnmatch
        """

        name = op.GetName()

        if not fnmatch(name, self._name_pattern):
            """
            Append error message to messagebag
            """
            raise Exception(
                "Object must match pattern '{}' is '{}'".format(
                    self._name_pattern,
                    name
                )
            )
        
        return True


class InstanceValidator(IValidator):

    def __init__(
        self,
        instance_type: c4d.BaseObject
    ) -> None:
        self._instance_type = instance_type
    
    def Validate(
        self,
        op: c4d.BaseObject
    ) -> bool:
        """
        Validate the given name string against the name pattern
        using fnmatch
        """

        if not isinstance(op, self._instance_type):
            """
            Append error message to messagebag
            """
            raise Exception(
                "Object must be an instance of '{}' is '{}'".format(
                    self._instance_type,
                    type(op)
                )
            )
        
        return True
