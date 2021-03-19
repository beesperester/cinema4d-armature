from __future__ import annotations

import c4d

from typing import Any, List, Optional


class Hierarchy:
    def __init__(
        self,
        name: str,
        op: c4d.BaseObject,
        children: Optional[List[Hierarchy]] = None,
    ) -> None:
        if children is None:
            children = []

        self._name: str = name
        self._op: c4d.BaseObject = op
        self._children: List[Hierarchy] = children

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__, self.GetName(), hex(id(self))
        )

    def __getattr__(self, name: str) -> Any:
        node_names: List[str] = [x.GetName() for x in self.GetChildren()]

        if name in node_names:
            return self.GetChildren()[node_names.index(name)]

        raise AttributeError(
            "{} has no attribute '{}'".format(
                "{}.{}".format(__name__, self.__class__.__name__), name
            )
        )

    def GetName(self) -> str:
        return self._name

    def SetName(self, name: str) -> None:
        assert isinstance(name, str)

        self._name = name

    def GetChildren(self) -> List[Hierarchy]:
        return self._children

    def GetObject(self) -> c4d.BaseObject:
        return self._op
