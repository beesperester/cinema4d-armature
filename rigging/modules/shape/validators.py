from __future__ import annotations

import c4d
import logging

from json import dumps
from fnmatch import fnmatch
from typing import List, TYPE_CHECKING

from rigging.utilities.iterator import IterateChildren
from rigging.modules.messagebag import Messagebag, Message


if TYPE_CHECKING:
    from rigging.modules.shape import Shape


class ValidationError(Exception):
    """
    This class represents a validation error
    """


class IValidator:

    def Validate(
        self,
        op: c4d.BaseObject,
        messagebag: Messagebag
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
        op: c4d.BaseObject,
        messagebag: Messagebag
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
            message = Message(
                "Name must match pattern '{}' is '{}'".format(
                    self._name_pattern,
                    name
                )
            )

            logging.warning(message.GetMessage())

            messagebag.append(message)

            return False
        
        return True
    
    def GetShape(self):
        return {
            "type": self.__class__.__name__,
            "data": self._name_pattern
        }


class InstanceValidator(IValidator):

    def __init__(
        self,
        instance_type: c4d.BaseObject
    ) -> None:
        self._instance_type = instance_type
    
    def Validate(
        self,
        op: c4d.BaseObject,
        messagebag: Messagebag
    ) -> bool:
        """
        Validate the given name string against the name pattern
        using fnmatch
        """

        if not isinstance(op, self._instance_type):
            """
            Append error message to messagebag
            """
            message = Message(
                "Object must be an instance of '{}' is '{}'".format(
                    self._instance_type,
                    type(op)
                )
            )

            logging.warning(message.GetMessage())

            messagebag.append(message)

            return False
        
        return True
    
    def GetShape(self):
        return {
            "type": self.__class__.__name__,
            "data": self._instance_type.__name__
        }


class ChildrenValidator(IValidator):

    def __init__(
        self,
        children: List["ObjectShape"]
    ) -> None:
        self._children = children
    
    def Validate(
        self,
        op: c4d.BaseObject,
        messagebag: Messagebag
    ) -> bool:            
        is_valid = []
        
        for child_object_shape in self._children:
            is_valid.append(any([
                child_object_shape.Validate(x, messagebag)
                for x in IterateChildren(op.GetDown())
            ]))
        
        if len(is_valid) > 0 and not any(is_valid):
            message = Message(
                "Object children must match shape of\n'{}'".format(
                    dumps(self.GetShape(), indent=2)
                )
            )

            logging.warning(message.GetMessage())

            messagebag.append(message)

            return False
        
        return True
    
    def GetShape(self):
        """
        Get shape of children validator
        """

        return {
            "type": self.__class__.__name__,
            "data": [x.GetShape() for x in self._children]
        }


def ValidateAndRaise(
    op: c4d.BaseObject,
    shape: Shape
) -> bool:
    messagebag = Messagebag()
    
    if not shape.Validate(op, messagebag):
        for message in messagebag:
            raise ValidationError(message.GetMessage())
    
    return True
