from mock4d.baselist2d import BaseList2D
from mock4d.gelistnode import GeListNode


class LayerObject(BaseList2D):
    """
    This class represents a Layer Object
    """

class BaseDocument(BaseList2D):
    """
    This class represents a Base Document
    """

    def __init__(
        self,
        atom_type: int = None
    ) -> None:
        self._layers = GeListNode()

        super(BaseDocument, self).__init__(atom_type)

    def GetLayerObjectRoot(self):
        return self._layers