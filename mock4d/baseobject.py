from __future__ import annotations

from typing import List, Optional

from mock4d import baselist2d, basetag


class BaseObject(baselist2d.BaseList2D):
    """
    This class represents a Base Object
    """

    def __init__(
        self,
        atom_type: int
    ) -> None:
        self._tags = []

        super(BaseObject, self).__init__(atom_type)

    def GetTags(self) -> List[basetag.BaseTag]:
        return self._tags

    def InsertTag(
        self,
        tp: basetag.BaseTag,
        pred: Optional[basetag.BaseTag] = None
    ) -> None:
        assert isinstance(tp, basetag.BaseTag)

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
        pred: Optional[basetag.BaseTag] = None
    ) -> basetag.BaseTag:
        tag = basetag.BaseTag(x)

        tag.SetObject(self)

        self.InsertTag(tag, pred)

        return tag
