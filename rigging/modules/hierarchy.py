import c4d

from typing import Any, List


class Hierarchy:

    def __init__(
        self,
        name: str,
        op: c4d.BaseObject,
        children: List["Hierarchy"] = None
    ) -> None:
        if children is None:
            children = []

        self._name = name
        self._op = op
        self._children = children
    
    def __repr__(self):
        return "<{}.{} object '{}'>".format(
            __name__,
            self.__class__.__name__,
            self.GetName()
        )
    
    def __getattr__(
        self,
        name: str
    ) -> Any:
        node_names = [x.GetName() for x in self.GetChildren()]

        if name in node_names:
            return self.GetChildren()[node_names.index(name)]
        
        raise AttributeError(
            "{} has no attribute '{}'".format(
                "{}.{}".format(__name__, self.__class__.__name__),
                name
            )
        )
    
    def GetName(self) -> str:
        return self._name
    
    def GetChildren(self):
        return self._children
    
    def GetObject(self) -> c4d.BaseObject:
        return self._op