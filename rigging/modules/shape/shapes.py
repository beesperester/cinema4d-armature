from __future__ import annotations

import mock4d as c4d

from typing import List, Any, TYPE_CHECKING

from rigging.modules.hierarchy import Hierarchy
from rigging.utilities.iterator import IterateChildren

if TYPE_CHECKING:
    from rigging.modules.validators import IValidator


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
        validators: List[IValidator] = None,
        children: List[Shape] = None
    ) -> None:
        if validators is None:
            validators = []
        
        if children is None:
            children = []

        self._name = name
        self._validators = validators
        self._children = children
    
    def __repr__(self):
        return "<{}.{} object '{}'>".format(
            __name__,
            self.__class__.__name__,
            self.GetName()
        )
    
    def GetValidators(self) -> List[IValidator]:
        return [*self._validators]
    
    def GetChildren(self) -> List[Shape]:
        return [*self._children]
    
    def GetName(self) -> str:
        return self._name
    
    def Integrate(
        self,
        op: c4d.BaseObject
    ) -> bool:
        # test if self is valid
        for validator in self.GetValidators():
            validator.Validate(op)

        # test if child shapes are valid
        results = []
        exceptions = []

        for child_object_shape in self.GetChildren():
            for child_object in IterateChildren(op.GetDown()):
                try:
                    results.append(
                        child_object_shape.Integrate(child_object)
                    )
                except Exception as e:
                    exceptions.append(e)

        children_valid = (
            bool(results)
            if self.GetChildren() else True
        )
        
        if not children_valid:
            if exceptions:
                # no object matching specified shape
                raise Exception(exceptions.pop())
            else:
                # missing object
                raise Exception("No child object matches shape")
        
        return Hierarchy(
            self.GetName(),
            op,
            results
        )
