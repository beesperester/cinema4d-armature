import c4d

from typing import List, Any

from rigging.modules.messagebag import Messagebag
from rigging.modules.shape.validators import ChildrenValidator


class ShapeError(Exception):
    """
    This class represents a shape error
    """


class Shape:
    """
    This class represents a shape
    """

    def GetShape(self):
        raise NotImplementedError("Method 'GetShape' is not implemented")



class ObjectShape(Shape):

    def __init__(
        self,
        name: str,
        validators: List["IValidator"] = None
    ) -> None:
        if validators is None:
            validators = []

        self._name = name
        self._validators = validators
    
    def __repr__(self):
        return "<{}.{} object '{}'>".format(
            __name__,
            self.__class__.__name__,
            self.GetName()
        )
    
    def GetValidators(self) -> List["IValidator"]:
        return self._validators
    
    def GetName(self) -> str:
        return self._name

    def GetShape(self):
        return {
            "type": self.__class__.__name__,
            "name": self.GetName(),
            "validators": [
                x.GetShape() for x in self.GetValidators()
            ]
        }
    
    def Validate(
        self,
        op: c4d.BaseObject,
        messagebag: Messagebag
    ) -> bool:

        return all([
            x.Validate(op, messagebag)
            for x in self.GetValidators()
        ])





