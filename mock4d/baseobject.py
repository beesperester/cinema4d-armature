from __future__ import annotations

from typing import List, Optional

from mock4d import baselist2d
from mock4d import interfaces
from mock4d.math import Vector, Matrix


class BaseObject(interfaces.IBaseObject, baselist2d.BaseList2D):
    """
    This class represents a Base Object
    """

    def __init__(
        self,
        atom_type: int
    ) -> None:
        self._tags: List[interfaces.IBaseTag] = []

        super(BaseObject, self).__init__(atom_type)

    def GetTags(self) -> List[interfaces.IBaseTag]:
        return self._tags

    def InsertTag(
        self,
        tp: interfaces.IBaseTag,
        pred: Optional[interfaces.IBaseTag] = None
    ) -> None:
        assert isinstance(tp, interfaces.IBaseTag)

        if pred in self._tags:
            self._tags.insert(
                self._tags.index(pred) + 1,
                tp
            )
        else:
            self._tags.append(tp)

        tp.SetObject(self)

    def MakeTag(
        self,
        x: int,
        pred: Optional[interfaces.IBaseTag] = None
    ) -> interfaces.IBaseTag:
        tag = interfaces.IBaseTag(x)

        tag.SetObject(self)

        self.InsertTag(tag, pred)

        return tag

    def GetMg(self) -> Matrix:
        return Matrix(
            Vector(1, 0, 0),
            Vector(0, 1, 0),
            Vector(0, 0, 1),
            Vector(0)
        )

    def SetMg(self, matrix: Matrix) -> None:
        pass

    def GetMl(self) -> Matrix:
        return self.GetMg()

    def SetMl(self, matrix: Matrix) -> None:
        pass
