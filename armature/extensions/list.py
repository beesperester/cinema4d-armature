from typing import Optional, TypeVar, Generic, List, Any


from armature.interfaces import INamed
from armature.decorators import dont_use

T = TypeVar("T", bound=INamed, covariant=True)


class AcessibleList(List[T]):
    def __init__(self, items: Optional[List[T]] = None) -> None:
        if items is None:
            items = list()

        self.data = items

    def Get(self, name: str) -> T:
        if name in self.GetNames():
            return self.data[self.GetNames().index(name)]

        raise Exception(
            "{} has no item '{}'".format(self.__class__.__name__, name)
        )

    def GetNames(self) -> List[str]:
        return [x.GetName() for x in self.data]

    def Extend(self, items: List[T]) -> None:
        self.data.extend(items)

    def extend(self, items: List[T]) -> None:
        raise Exception("Don't use this method. Use Extend instead.")
