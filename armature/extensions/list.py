from typing import Optional, TypeVar, Generic, List, Any, MutableSequence


from armature.interfaces import INamed

T = TypeVar("T", bound=INamed)


class AcessibleList(Generic[T]):
    def __init__(self, items: Optional[List[T]] = None) -> None:
        if items is None:
            items = list()

        self.data = items
        self.n = 0

    def __iter__(self):
        self.n = 0

        return self

    def __next__(self) -> T:
        if self.n < len(self.data):
            result = self.data[self.n]

            self.n += 1

            return result
        else:
            raise StopIteration

    def Append(self, item: T) -> None:
        self.data.append(item)

    def Get(self, name: str) -> T:
        if name in self.GetNames():
            return self.data[self.GetNames().index(name)]

        raise Exception(
            "{} has no item '{}'".format(self.__class__.__name__, name)
        )

    def GetNames(self) -> List[str]:
        return [x.GetName() for x in self.data]

    def Extend(self, items: "AcessibleList[T]") -> None:
        self.data.extend(items.data)
