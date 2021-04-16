from __future__ import annotations

import c4d
import typing
import fnmatch

from collections import UserList, abc
from typing import (
    Generator,
    List,
    Optional,
    Dict,
    Any,
    TypeVar,
    Generic,
    Type,
    Union,
    Sequence,
    Iterable,
    MutableSequence,
)


class DagNotFoundError(Exception):
    pass


class DagAtom:
    def __init__(self, item: c4d.BaseList2D) -> None:
        self.item = item
        self._is_alive = True

    def __repr__(self):
        return "<{} named '{}' with id #{} at {}>".format(
            self.__class__.__name__,
            self.GetName(),
            self.GetType(),
            hex(id(self)),
        )

    def IsAlive(self) -> bool:
        return self._is_alive

    def Remove(self) -> None:
        self.item.Remove()
        self._is_alive = False

    def GetName(self) -> str:
        return self.item.GetName()  # type: ignore

    def GetType(self) -> int:
        return self.item.GetType()  # type: ignore


class DagBaseObject(DagAtom):
    item: c4d.BaseObject

    def GetChildren(self) -> DagAtomList[DagBaseObject]:
        children: List[c4d.BaseObject] = self.item.GetChildren()  # type: ignore

        return DagAtomList([DagBaseObject(x) for x in children])

    def GetParent(self) -> DagBaseObject:
        parent: c4d.BaseObject = self.item.GetUp()  # type: ignore

        return DagBaseObject(parent)

    def GetRecursive(self, path: str) -> Generator[DagBaseObject, None, None]:
        child = self.GetChild(path)

        yield child

        try:
            yield from child.GetRecursive(path)
        except DagNotFoundError:
            pass

    def GetChild(self, path: str) -> DagBaseObject:
        parts = path.split("/")

        child = self.GetChildren().Get(path)

        if len(parts) > 1:
            return child.GetChild("/".join(parts[1:]))

        return child

    def GetTags(self) -> DagAtomList[DagBaseTag]:
        tags: List[c4d.BaseTag] = self.item.GetTags()  # type: ignore

        return DagAtomList([DagBaseTag(x) for x in tags])

    def GetTag(self, path: str) -> DagBaseTag:
        return self.GetTags().Get(path)


class DagBaseTag(DagAtom):
    item: c4d.BaseTag


T = TypeVar("T", bound=DagAtom)


class DagAtomList(Generic[T], abc.MutableSequence):
    def __init__(self, items: Optional[MutableSequence[T]] = None) -> None:
        if items is None:
            items = []

        self._items = items
        self._n = 0

    def __delitem__(self, index: int) -> None:
        self.CleanUp()

        del self._items[index]

    def __getitem__(self, index: int) -> T:
        self.CleanUp()

        return self._items[index]

    def __len__(self) -> int:
        self.CleanUp()

        return len(self._items)

    def __iter__(self):
        self.CleanUp()

        self._n = 0

        return self

    def __next__(self) -> T:
        if self._n < len(self._items):
            result = self._items[self._n]

            self._n += 1

            return result
        else:
            raise StopIteration

    def __setitem__(self, index: int, item: T) -> None:
        self.CleanUp()

        self._items[index] = item

    # mutable sequence default functions

    def insert(self, index: int, item: T) -> None:
        self.CleanUp()

        self._items.insert(index, item)

    def extend(self, items: MutableSequence[T]) -> None:
        self.CleanUp()

        self._items.extend(items)

    def append(self, item: T) -> None:
        self.CleanUp()

        self._items.append(item)

    def pop(self, index: Optional[int] = None) -> T:
        if index is None:
            return self._items.pop()

        return self._items.pop(index)

    # sugar functions

    def Insert(self, index: int, item: T) -> None:
        self.insert(index, item)

    def Extend(self, items: MutableSequence[T]) -> None:
        self.extend(items)

    def Append(self, item: T) -> None:
        self.append(item)

    def Pop(self, index: Optional[int] = None) -> T:
        return self.pop(index)

    # custom functions

    def CleanUp(self):
        self._items = list(filter(lambda x: x.IsAlive(), self._items))

    def Get(self, path: str) -> T:
        self.CleanUp()

        names: List[str] = [x.GetName() for x in self._items]

        parts = path.split("/")

        if len(parts) > 0:
            name = parts[0]
            child_index = -1

            # use fnmatch against the list of child names
            # if name contains an asterisk
            if "*" in name:
                matching_child_names = fnmatch.filter(names, name)

                if matching_child_names:
                    child_index = names.index(matching_child_names[0])
            # use name as is against list of child names
            else:
                if name in names:
                    child_index = names.index(name)

            # use child index to retrieve base object
            # if child index is larger -1
            if child_index > -1:
                child = self._items[child_index]

                return child

        raise DagNotFoundError(
            f"'{self.__class__.__name__}' has no child object called '{path}'"
        )


class DagBaseObjectList(DagAtomList[DagBaseObject]):
    pass


class DagBaseTagList(DagAtomList[DagBaseTag]):
    pass
