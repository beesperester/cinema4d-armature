from __future__ import annotations

import c4d

from typing import Any, List, Optional, Generator


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

    def GetName(self) -> str:
        return self._name

    def SetName(self, name: str) -> None:
        assert isinstance(name, str)

        self._name = name

    def GetChildren(self) -> List[Hierarchy]:
        return self._children

    def GetChild(self, name: str) -> Hierarchy:
        node_names: List[str] = [x.GetName() for x in self.GetChildren()]

        if name in node_names:
            return self.GetChildren()[node_names.index(name)]

        raise Exception("{} has no child '{}'".format(self.GetName(), name))

    def GetObject(self) -> c4d.BaseObject:
        return self._op

    def GetRecursive(self, name: str) -> Generator[Hierarchy, None, None]:
        try:
            child = self.GetChild(name)

            yield child

            yield from child.GetRecursive(name)
        except Exception:
            pass
