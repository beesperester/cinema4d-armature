from __future__ import annotations

import c4d
import typing
import fnmatch

from typing import Generator, List, Optional, Dict, Any, TypeVar, Generic


T = TypeVar("T", bound=c4d.BaseList2D, contravariant=True)


class DagNotFoundError(Exception):
    pass


class DagBaseList2D(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item

    def __repr__(self):
        return "<{} named '{}' with id #{} at {}>".format(
            self.__class__.__name__,
            self.GetName(),
            self.GetType(),
            hex(id(self)),
        )

    def GetName(self) -> str:
        return self.item.GetName()  # type: ignore

    def GetType(self) -> int:
        return self.item.GetType()  # type: ignore

    def GetChildren(self) -> DagBaseList2DList[T]:
        children: List[T] = self.item.GetChildren()  # type: ignore

        return DagBaseList2DList(children)

    def GetChild(self, path: str) -> DagBaseList2D[T]:
        return self.GetChildren().Get(path)

    def GetParent(self) -> DagBaseList2D[T]:
        parent: T = self.item.GetUp()  # type: ignore

        return DagBaseList2D(parent)

    def GetRecursive(
        self, path: str
    ) -> Generator[DagBaseList2D[T], None, None]:
        child = self.GetChild(path)

        yield child

        try:
            yield from child.GetRecursive(path)
        except DagNotFoundError:
            pass


class DagBaseObject(DagBaseList2D[c4d.BaseObject]):
    def GetChildren(self) -> DagBaseObjectList:
        children: List[c4d.BaseObject] = self.item.GetChildren()  # type: ignore

        return DagBaseObjectList(children)

    def GetChild(self, path: str) -> DagBaseObject:
        return DagBaseObject(super().GetChild(path).item)

    def GetParent(self) -> DagBaseObject:
        return DagBaseObject(super().GetParent().item)

    def GetTags(self) -> DagBaseTagList:
        tags: List[c4d.BaseTag] = self.item.GetTags()  # type: ignore

        return DagBaseTagList(tags)

    def GetTag(self, path: str) -> DagBaseTag:
        return self.GetTags().Get(path)

    def GetRecursive(self, path: str) -> Generator[DagBaseObject, None, None]:
        for result in super().GetRecursive(path):
            yield DagBaseObject(result.item)


class DagBaseTag(DagBaseList2D[c4d.BaseTag]):
    pass


class DagBaseList2DList(Generic[T]):
    def __init__(self, items: Optional[List[T]] = None) -> None:
        if items is None:
            items = []

        self.items = items
        self._n = 0

    def __iter__(self):
        self._n = 0

        return self

    def __next__(self) -> DagBaseList2D[T]:
        if self._n < len(self.items):
            result = self.items[self._n]

            self._n += 1

            return self.__wrapitem__(result)
        else:
            raise StopIteration

    def __getitem__(self, index: int) -> DagBaseList2D[T]:
        return self.__wrapitem__(self.items[index])

    def __wrapitem__(self, item: T) -> DagBaseList2D[T]:
        return DagBaseList2D(item)

    def Get(self, path: str) -> DagBaseList2D[T]:
        names: List[str] = [x.GetName() for x in self]  # type: ignore

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
                child = self[child_index]

                if len(parts) > 1:
                    return child.GetChild("/".join(parts[1:]))
                else:
                    return child

        raise DagNotFoundError(
            f"'{self.__class__.__name__}' has no child object called '{path}'"
        )

    def Extend(self, items: DagBaseList2DList[T]) -> None:
        self.items.extend(items.items)

    def Append(self, item: DagBaseList2D[T]) -> None:
        self.items.append(item.item)


class DagBaseObjectList(DagBaseList2DList[c4d.BaseObject]):
    def __getitem__(self, index: int) -> DagBaseObject:
        return DagBaseObject(super().__getitem__(index).item)

    def __wrapitem__(self, item: c4d.BaseObject) -> DagBaseObject:
        return DagBaseObject(item)

    def Extend(self, items: DagBaseObjectList) -> None:
        return super().Extend(items)

    def Append(self, item: DagBaseObject) -> None:
        super().Append(item)

    def Get(self, path: str) -> DagBaseObject:
        return DagBaseObject(super().Get(path).item)


class DagBaseTagList(DagBaseList2DList[c4d.BaseTag]):
    def __getitem__(self, index: int) -> DagBaseTag:
        return DagBaseTag(super().__getitem__(index).item)

    def __wrapitem__(self, item: c4d.BaseTag) -> DagBaseTag:
        return DagBaseTag(item)

    def Extend(self, items: DagBaseTagList) -> None:
        return super().Extend(items)

    def Append(self, item: DagBaseTag) -> None:
        super().Append(item)

    def Get(self, path: str) -> DagBaseTag:
        return DagBaseTag(super().Get(path).item)
