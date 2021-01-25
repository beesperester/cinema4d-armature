from __future__ import annotations

from mock4d import gelistnode


class LayerObject:
    """
    This class represents a Layer Object
    """


class BaseDocument:
    """
    This class represents a Base Document
    """

    def __init__(
        self,
    ) -> None:
        self._layers: gelistnode.GeListNode = gelistnode.GeListNode()

    def GetLayerObjectRoot(self) -> gelistnode.GeListNode:
        return self._layers
