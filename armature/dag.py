import c4d
import typing
import fnmatch

from typing import List, Optional, Dict, Any


class DagObject:
    def __init__(self, op: c4d.BaseObject) -> None:
        self._op = op

    def __repr__(self):
        return "<{} named '{}' with id #{} at {}>".format(
            self.__class__.__name__,
            self.GetObject().GetName(),
            self.GetObject().GetType(),
            hex(id(self)),
        )

    def GetObject(self) -> c4d.BaseObject:
        return self._op

    def Get(self, path: str) -> "DagObject":
        return self.GetChildren().Get(path)

    def GetRecursive(
        self, path: str
    ) -> typing.Generator["DagObject", None, None]:
        try:
            child = self.Get(path)

            yield child

            yield from child.GetRecursive(path)
        except Exception:
            pass

    def GetChildren(self) -> "DagObjects":
        children: List[c4d.BaseObject] = self.GetObject().GetChildren()  # type: ignore

        return DagObjectsFromBaseObjects(children)


class DagObjects:
    def __init__(self, items: Optional[List[DagObject]] = None) -> None:
        if items is None:
            items = []

        self._items = items
        self.n = 0

    def __iter__(self):
        self.n = 0

        return self

    def __next__(self) -> DagObject:
        if self.n < len(self._items):
            result = self._items[self.n]

            self.n += 1

            return result
        else:
            raise StopIteration

    def __getitem__(self, index: int) -> DagObject:
        return self._items[index]

    def Get(self, path: str) -> DagObject:
        child_names: typing.List[str] = [
            x.GetObject().GetName() for x in self._items
        ]  # type: ignore

        parts = path.split("/")

        if len(parts) > 0:
            name = parts[0]
            child_index = -1

            # use fnmatch against the list of child names
            # if name contains an asterisk
            if "*" in name:
                matching_child_names = fnmatch.filter(child_names, name)

                if matching_child_names:
                    child_index = child_names.index(matching_child_names[0])
            # use name as is against list of child names
            else:
                if name in child_names:
                    child_index = child_names.index(name)

            # use child index to retrieve base object
            # if child index is larger -1
            if child_index > -1:
                child = self._items[child_index]

                if len(parts) > 1:
                    return child.Get("/".join(parts[1:]))
                else:
                    return child

        raise Exception(
            "'{}' has no child object called '{}'".format(
                self.__class__.__name__, path
            )
        )

    def Extend(self, dag_objects: "DagObjects") -> "DagObjects":
        self._items.extend(dag_objects._items)

        return self

    def Append(self, dag_object: DagObject) -> "DagObjects":
        self._items.append(dag_object)

        return self


def DagObjectFromBaseObject(op: c4d.BaseObject) -> DagObject:
    return DagObject(op)


def DagObjectsFromBaseObjects(items: List[c4d.BaseObject]) -> DagObjects:
    return DagObjects([DagObject(x) for x in items])


def SerializeVectorAsDict(vector: c4d.Vector) -> Dict[str, float]:
    return {"x": vector.x, "y": vector.y, "z": vector.z}  # type: ignore


def SerializeMatrixAsDict(matrix: c4d.Matrix) -> Dict[str, Dict]:
    return {
        "off": SerializeVectorAsDict(matrix.off),  # type: ignore
        "v1": SerializeVectorAsDict(matrix.v1),  # type: ignore
        "v2": SerializeVectorAsDict(matrix.v2),  # type: ignore
        "v3": SerializeVectorAsDict(matrix.v3),  # type: ignore
    }


def SerializeDagObjectAsDict(item: DagObject) -> Dict[str, Any]:
    base_object = item.GetObject()

    return {
        "name": base_object.GetName(),
        "type": base_object.GetType(),
        "matrix": SerializeMatrixAsDict(base_object.GetMg()),  # type: ignore
        "children": SerializeDagObjectsAsList(item.GetChildren()),
        "tags": SerializeTagObjectsAsList(base_object.GetTags()),  # type: ignore
    }


def SerializeTagObjectAsDict(tag: c4d.BaseTag) -> Dict[str, Any]:
    return {}


def SerializeTagObjectsAsList(tags: List[c4d.BaseTag]) -> List[Dict[str, Any]]:
    return [SerializeTagObjectAsDict(x) for x in tags]


def SerializeDagObjectsAsList(items: DagObjects) -> List[Dict]:
    return [SerializeDagObjectAsDict(x) for x in items]


def CreateDagObject(
    name: str, object_type: int, children: Optional[DagObjects] = None
) -> DagObject:
    if children is None:
        children = DagObjects()

    base_object = c4d.BaseObject(object_type)
    base_object.SetName(name)

    for child in children:
        child.GetObject().InsertUnder(base_object)

    return DagObjectFromBaseObject(base_object)
