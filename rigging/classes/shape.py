import c4d

from json import dumps
from typing import List
from fnmatch import fnmatch

from iterators import IterateChildren


class ShapeError(Exception):
    """
    This class represents a shape error
    """


class Messages(list):
    """
    This class represents validation messages
    """


class NameShape:
    """
    This class represents the shape name should have
    """

    def __init__(
        self,
        name_pattern: str
    ) -> None:
        self._name_pattern = name_pattern
        self._messages = []
    
    def __repr__(self) -> str:
        return "<{}.{} object '{}'>".format(
            __name__,
            self.__class__.__name__,
            self.GetNamePattern()
        )

    def GetNamePattern(self) -> str:
        """
        Get the name pattern
        """
        return self._name_pattern
    
    def Validate(
        self,
        name: str,
        messages: Messages = None
    ) -> bool:
        """
        Validate the given name string against the name pattern
        using fnmatch
        """
        if messages is None:
            """
            Use own messages
            if no messages object is provided
            """
            messages = self._messages

        if not fnmatch(name, self._name_pattern):
            """
            Append error message to messages
            """
            messages.append(
                "Name must match pattern '{}' is '{}'".format(
                    self._name_pattern,
                    name
                )
            )

            return False
        
        return True
    
    def GetShape(self):
        """
        Get shape of object
        """
        return self._name_pattern    


class ObjectShape:

    def __init__(
        self,
        name: str,
        name_shape: NameShape,
        instance_type: c4d.BaseObject,
        children: List["ObjectShape"] = None
    ) -> None:
        self._name = name
        self._name_shape = name_shape
        self._instance_type = instance_type
        self._messages = Messages()
        self._op = None

        if children is None:
            children = []

        self._children = children
    
    def __repr__(self):
        return "<{}.{} object '{}'>".format(
            __name__,
            self.__class__.__name__,
            self.GetName()
        )
    
    def __getattr__(self, name):
        children_names = [x.GetName() for x in self.GetChildren()]

        if name in children_names:
            return self.GetChildren()[children_names.index(name)]
        
        raise AttributeError("{} has no attribute '{}'".format(
            type(self),
            name
        ))
    
    @classmethod
    def GetObjectShape(cls, op: c4d.BaseObject):
        return {
            "name": op.GetName(),
            "instance_type": op.__class__.__name__,
            "children": [
                cls.GetObjectShape(x) for x in IterateChildren(op.GetDown())
            ]
        }
    
    def GetChildren(self):
        return [*self._children]
    
    def GetName(self):
        return self._name
    
    def GetObject(self):
        return self._op
    
    def Validate(
        self,
        op: c4d.BaseObject,
        messages: Messages = None
    ) -> bool:
        if messages is None:
            """
            Use own messages
            if no messages object is provided
            """
            messages = self._messages

        if not isinstance(op, self._instance_type):
            """
            Append error message to messages
            """
            messages.append(
                "Object must be an instance of '{}' is '{}'".format(
                    self._instance_type,
                    type(op)
                )
            )

            return False
        
        if not self._name_shape.Validate(op.GetName(), messages):
            """
            
            """
            return False           
        
        is_valid = []
        
        for child_shape in self._children:
            is_valid.append(any([
                child_shape.Validate(x, messages)
                for x in IterateChildren(op.GetDown())
            ]))
        
        if len(is_valid) > 0 and not any(is_valid):
            messages.append(
                "Object children must match shape of\n'{}'\nbut is\n'{}'".format(
                    dumps(self.GetShape(), indent=2),
                    dumps(self.GetObjectShape(op), indent=2)
                )
            )

            return False
        
        self._op = op

        return True
    
    def GetShape(self):
        """
        Get shape of object
        """

        return {
            "name_shape": self._name_shape.GetShape(),
            "instance_type": self._instance_type.__name__,
            "children": [x.GetShape() for x in self._children]
        }

    def GetMessages(self):
        return [*self._messages]


class Shape:

    def __init__(
        self,
        object_shape: ObjectShape
    ) -> None:
        self._object_shape = object_shape
        self._messages = Messages()

    def GetMessages(self):
        return self._messages
    
    def Validate(self, op: c4d.BaseObject):
        if not self._object_shape.Validate(op, self._messages):
            for message in self._messages:
                raise ShapeError(message)
        
        return True


def EvaluateMessages(object_shape: ObjectShape):
    for message in object_shape.GetMessages():
        raise ShapeError(message)
