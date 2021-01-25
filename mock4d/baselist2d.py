from __future__ import annotations

import copy

from typing import Optional

from mock4d.gelistnode import GeListNode
from mock4d.basecontainer import BaseContainer
from mock4d import interfaces


class BaseList2D(GeListNode):
    """
    This class represents a Base List 2D
    """

    def __init__(
        self,
        atom_type: Optional[int] = None
    ) -> None:
        self._name: str = ""
        self._layer: Optional[interfaces.ILayerObject] = None

        super(BaseList2D, self).__init__(atom_type)

    def __repr__(self) -> str:
        object_name: str = "{}/{}".format(
            self.GetTypeName(),
            self.GetName()
        )

        return "<{} {} with id '{}' at {}>".format(
            self.__class__.__name__,
            object_name,
            self.GetType(),
            hex(id(self))
        )

    def GetData(self) -> BaseContainer:
        return copy.deepcopy(self.GetDataInstance())

    def GetDataInstance(self) -> BaseContainer:
        return self._data

    def SetName(self, name: str):
        assert isinstance(name, str)

        self._name = name

    def GetName(self) -> str:
        return self._name

    def SetLayerObject(
        self,
        layer: interfaces.ILayerObject
    ) -> None:
        self._layer = layer

    def GetLayerObject(
        self,
        doc: interfaces.IBaseDocument
    ) -> Optional[interfaces.ILayerObject]:
        return self._layer
