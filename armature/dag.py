import c4d

from typing import List, Optional


class DagItem:
    def __init__(self, op: c4d.BaseObject, name: Optional[str] = None) -> None:
        self._op = op
        self._name = name

    def GetObject(self) -> c4d.BaseObject:
        return self._op

    def GetName(self) -> str:
        if self._name:
            return self._name

        return self.GetObject().GetName()  # type: ignore

    def Get(self, path: str) -> "DagItem":
        children: List[c4d.BaseObject] = self.GetObject().GetChildren()  # type: ignore

        child_names = [x.GetName() for x in children]

        parts = path.split("/")

        if len(parts) > 0:
            name = parts[0]

            if name in child_names:
                child = DagItem(children[child_names.index(name)])

                if len(parts) > 1:
                    return child.Get("/".join(parts[1:]))
                else:
                    return child

        raise Exception(
            "'{}' has no child object called '{}'".format(
                self.__class__.__name__, path
            )
        )


class DagItems:
    def __init__(self, items: Optional[List[DagItem]] = None) -> None:
        if items is None:
            items = []

        self._items = items

    def Get(self, path: str) -> DagItem:
        child_names = [x.GetName() for x in self._items]

        parts = path.split("/")

        if len(parts) > 0:
            name = parts[0]

            if name in child_names:
                child = self._items[child_names.index(name)]

                if len(parts) > 1:
                    return child.Get("/".join(parts[1:]))
                else:
                    return child

        raise Exception(
            "'{}' has no child object called '{}'".format(
                self.__class__.__name__, path
            )
        )


def DagItemsFromBaseObjects(items: List[c4d.BaseObject]) -> DagItems:
    return DagItems([DagItem(x) for x in items])
