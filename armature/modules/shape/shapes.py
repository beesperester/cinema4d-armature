from __future__ import annotations

import c4d

from typing import List, Optional

from armature.modules.hierarchy import Hierarchy

from armature.modules.shape import interfaces


class BaseShape(interfaces.IShape):
    """
    This class represents a Shape
    """

    def __init__(
        self,
        name: str,
        validators: Optional[List[interfaces.IValidator]] = None
    ) -> None:
        if validators is None:
            validators = []

        self._name: str = name
        self._validators: List[interfaces.IValidator] = validators

    def __repr__(self):
        return "<{}.{} object '{}'>".format(
            __name__,
            self.__class__.__name__,
            self.GetName()
        )

    def GetValidators(self) -> List[interfaces.IValidator]:
        return self._validators

    def GetName(self) -> str:
        return self._name


class RecursiveShape(BaseShape):
    """
    This class represents a Recursive Shape
    """

    def __init__(
        self,
        shape: BaseShape
    ) -> None:
        self._shape = shape

    def GetShape(self):
        return self._shape

    def RecursiveExtract(
        self,
        op: c4d.BaseObject
    ) -> Hierarchy:
        hierarchy = self.GetShape().Extract(op)

        for child in hierarchy.GetObject().GetChildren():
            try:
                child_hierarchy = self.RecursiveExtract(child)

                hierarchy.GetChildren().append(child_hierarchy)
            except Exception:
                pass

        return hierarchy

    def Extract(
        self,
        op: c4d.BaseObject
    ) -> Hierarchy:
        return self.RecursiveExtract(op)


class ObjectShape(BaseShape):
    """
    This class represents an Object Shape
    """

    def __init__(
        self,
        name: str,
        validators: Optional[List[interfaces.IValidator]] = None,
        children: Optional[List[BaseShape]] = None
    ) -> None:
        if children is None:
            children = []

        self._children: List[BaseShape] = children

        super(ObjectShape, self).__init__(name, validators)

    def GetChildren(self) -> List[BaseShape]:
        return [*self._children]

    def Extract(
        self,
        op: c4d.BaseObject
    ) -> Hierarchy:
        # test if self is valid
        for validator in self.GetValidators():
            validator.Validate(op)

        # test if child shapes are valid
        results = []
        exceptions = []

        for child_object_shape in self.GetChildren():
            for child_object in op.GetChildren():
                try:
                    results.append(
                        child_object_shape.Extract(child_object)
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
