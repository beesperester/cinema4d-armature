from __future__ import annotations

import c4d

from fnmatch import fnmatch

from armature.modules.shape import interfaces


class ValidationError(Exception):
    """
    This class represents a validation error
    """


class NameValidator(interfaces.IValidator):

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


class InstanceValidator(interfaces.IValidator):

    def __init__(
        self,
        instance_type: int
    ) -> None:
        self._instance_type: int = instance_type

    def Validate(
        self,
        op: c4d.BaseObject
    ) -> bool:
        """
        Validate the given name string against the name pattern
        using fnmatch
        """

        if not op.IsInstanceOf(self._instance_type):
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
