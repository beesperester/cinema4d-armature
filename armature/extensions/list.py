from typing import Optional, TypeVar, Generic, List, Any


from armature.interfaces import INamed


T = TypeVar("T", Any, INamed)


class AcessibleList(List[T]):
    def __init__(self, items: Optional[List[T]] = None) -> None:
        if items is None:
            items = List[T]()

        self.data = items

    def Get(self, name: str) -> T:
        if name in self.GetNames():
            return self.data[self.GetNames().index(name)]

        raise Exception(
            "{} has no item '{}'".format(self.__class__.__name__, name)
        )

    def GetNames(self) -> List[str]:
        return [x.GetName() for x in self.data]
