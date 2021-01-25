from __future__ import annotations

from typing import List, Optional

from mock4d import baselist2d
from mock4d import interfaces


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
