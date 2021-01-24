from __future__ import annotations

from typing import Optional

from mock4d import baselist2d, gelistnode


class LayerObject(baselist2d.BaseList2D):
    """
    This class represents a Layer Object
    """


class BaseDocument(baselist2d.BaseList2D):
    """
    This class represents a Base Document
    """

    def __init__(
        self,
        atom_type: Optional[int] = None
    ) -> None:
        self._layers: gelistnode.GeListNode = gelistnode.GeListNode()

        super(BaseDocument, self).__init__(atom_type)

    def GetLayerObjectRoot(self):
        return self._layers
