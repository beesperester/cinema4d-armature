from __future__ import annotations

import c4d
import typing
import fnmatch

from typing import List, Optional, Dict, Any, TypeVar, Generic


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


class DagBaseObject(DagBaseList2D[c4d.BaseObject]):
    def GetChildren(self) -> DagBaseObjectList:
        children: List[c4d.BaseObject] = self.item.GetChildren()  # type: ignore

        return DagBaseObjectList(children)

    def GetChild(self, path: str) -> DagBaseObject:
        return DagBaseObject(super().GetChild(path).item)

    def GetTags(self) -> DagBaseTagList:
        tags: List[c4d.BaseTag] = self.item.GetTags()  # type: ignore

        return DagBaseTagList(tags)

    def GetTag(self, path: str) -> DagBaseTag:
        return self.GetTags().Get(path)


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


# class DagTag(DagBaseList2D[c4d.BaseTag]):
#     pass


# class DagObject(DagBaseList2D[c4d.BaseObject]):
#     def GetChild(self, path: str) -> "DagObject":
#         return self.GetChildren().Get(path)

#     def GetTag(self, name: str) -> DagTag:
#         return self.GetTags().Get(name)

#     def GetRecursive(
#         self, path: str
#     ) -> typing.Generator[DagObject, None, None]:
#         try:
#             child = self.GetChild(path)

#             yield child

#             yield from child.GetRecursive(path)
#         except Exception:
#             pass

#     def GetChildren(self) -> DagObjects:
#         children: List[c4d.BaseObject] = self.GetObject().GetChildren()  # type: ignore

#         return DagObjectsFromBaseObjects(children)

#     def GetTags(self) -> DagTags:
#         tags: List[c4d.BaseTag] = self.GetObject().GetTags()  # type: ignore

#         return DagTags([DagTag(x) for x in tags])


# class DagList(Generic[T]):
#     def __init__(self, items: Optional[List[T]] = None) -> None:
#         if items is None:
#             items = []

#         self._items = items
#         self._n = 0

#     def __iter__(self):
#         self._n = 0

#         return self

#     def __next__(self) -> T:
#         if self._n < len(self._items):
#             result = self._items[self._n]

#             self._n += 1

#             return result
#         else:
#             raise StopIteration

#     def __getitem__(self, index: int) -> T:
#         return self._items[index]

#     def Get(self, path: str) -> T:
#         raise NotImplementedError()

#     def Extend(self, items: DagList) -> None:
#         self._items.extend(items._items)

#     def Append(self, item: T) -> None:
#         self._items.append(item)


# class DagTags(DagList[c4d.BaseTag]):
#     def Get(self, path: str) -> DagTag:
#         tag_names: List[str] = [x.GetTag().GetName() for x in self._items]


# class DagObjects(DagList[DagObject]):
#     def Get(self, path: str) -> DagObject:
#         child_names: List[str] = [
#             x.GetObject().GetName() for x in self._items
#         ]  # type: ignore

#         parts = path.split("/")

#         if len(parts) > 0:
#             name = parts[0]
#             child_index = -1

#             # use fnmatch against the list of child names
#             # if name contains an asterisk
#             if "*" in name:
#                 matching_child_names = fnmatch.filter(child_names, name)

#                 if matching_child_names:
#                     child_index = child_names.index(matching_child_names[0])
#             # use name as is against list of child names
#             else:
#                 if name in child_names:
#                     child_index = child_names.index(name)

#             # use child index to retrieve base object
#             # if child index is larger -1
#             if child_index > -1:
#                 child = self._items[child_index]

#                 if len(parts) > 1:
#                     return child.GetChild("/".join(parts[1:]))
#                 else:
#                     return child

#         raise Exception(
#             "'{}' has no child object called '{}'".format(
#                 self.__class__.__name__, path
#             )
#         )


# def DagObjectFromBaseObject(op: c4d.BaseObject) -> DagObject:
#     return DagObject(op)


# def DagObjectsFromBaseObjects(items: List[c4d.BaseObject]) -> DagObjects:
#     return DagObjects([DagObject(x) for x in items])


# def SerializeVectorAsDict(vector: c4d.Vector) -> Dict[str, float]:
#     return {"x": vector.x, "y": vector.y, "z": vector.z}  # type: ignore


# def SerializeMatrixAsDict(matrix: c4d.Matrix) -> Dict[str, Dict]:
#     return {
#         "off": SerializeVectorAsDict(matrix.off),  # type: ignore
#         "v1": SerializeVectorAsDict(matrix.v1),  # type: ignore
#         "v2": SerializeVectorAsDict(matrix.v2),  # type: ignore
#         "v3": SerializeVectorAsDict(matrix.v3),  # type: ignore
#     }


# def SerializeDagObjectAsDict(item: DagObject) -> Dict[str, Any]:
#     base_object = item.GetObject()

#     return {
#         "name": base_object.GetName(),
#         "type": base_object.GetType(),
#         "matrix": SerializeMatrixAsDict(base_object.GetMg()),  # type: ignore
#         "children": SerializeDagObjectsAsList(item.GetChildren()),
#         "tags": SerializeTagObjectsAsList(base_object.GetTags()),  # type: ignore
#     }


# def SerializeTagObjectAsDict(tag: c4d.BaseTag) -> Dict[str, Any]:
#     return {}


# def SerializeTagObjectsAsList(tags: List[c4d.BaseTag]) -> List[Dict[str, Any]]:
#     return [SerializeTagObjectAsDict(x) for x in tags]


# def SerializeDagObjectsAsList(items: DagObjects) -> List[Dict]:
#     return [SerializeDagObjectAsDict(x) for x in items]


# def CreateDagObject(
#     name: str, object_type: int, children: Optional[DagObjects] = None
# ) -> DagObject:
#     if children is None:
#         children = DagObjects()

#     base_object = c4d.BaseObject(object_type)
#     base_object.SetName(name)

#     for child in children:
#         child.GetObject().InsertUnder(base_object)

#     return DagObjectFromBaseObject(base_object)
