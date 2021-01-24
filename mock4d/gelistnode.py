from __future__ import annotations

from typing import List, Optional, Any

from mock4d import c4datom, basecontainer


class GeListNode(c4datom.C4DAtom):
    """
    This class represents a Ge List Node
    """

    def __init__(
        self,
        atom_type: Optional[int] = None
    ) -> None:
        self._children: List[GeListNode] = []
        self._parent: Optional[GeListNode] = None
        self._data: basecontainer.BaseContainer = basecontainer.BaseContainer()

        super(GeListNode, self).__init__(atom_type)

    def __setitem__(self, key: str, value: Any):
        if not hasattr(self, key):
            self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        if not hasattr(self, key):
            return self._data[key]

    def GetDown(self):
        if self._children:
            return self._children[0]

        return None

    def GetUp(self) -> Optional[GeListNode]:
        return self._parent

    def GetChildren(self) -> List[GeListNode]:
        return self._children

    def GetNext(self: GeListNode) -> Optional[GeListNode]:
        if not self._parent:
            return None

        if not self._parent._children:
            return None

        own_index = self._parent._children.index(self)

        if own_index + 1 > len(self._parent._children) - 1:
            return None

        return self._parent._children[own_index + 1]

    def InsertUnder(
        self: GeListNode,
        parent: GeListNode
    ):
        self._parent = parent

        if self not in self._parent._children:
            self._parent._children.append(self)
