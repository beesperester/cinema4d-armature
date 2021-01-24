from __future__ import annotations

import copy

from typing import TYPE_CHECKING, Optional

from mock4d.gelistnode import GeListNode
from mock4d.basecontainer import BaseContainer

if TYPE_CHECKING:
    from mock4d import documents


class BaseList2D(GeListNode):
    """
    This class represents a Base List 2D
    """

    def __init__(
        self,
        atom_type: Optional[int] = None
    ) -> None:
        self._name: str = ""
        self._layer: Optional[documents.LayerObject] = None

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
        layer: documents.LayerObject
    ) -> None:
        self._layer = layer

    def GetLayerObject(
        self,
        doc: documents.BaseDocument
    ) -> Optional[documents.LayerObject]:
        return self._layer
