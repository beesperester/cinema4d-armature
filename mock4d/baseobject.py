from typing import List

from mock4d.baselist2d import BaseList2D
from mock4d.basetag import BaseTag


class BaseObject(BaseList2D):
    """
    This class represents a Base Object
    """

    def __init__(
        self,
        atom_type: int
    ) -> None:
        self._tags = []

        super(BaseObject, self).__init__(atom_type)
    
    def GetTags(self) -> List[BaseTag]:
        return self._tags

    def InsertTag(
        self,
        tp: BaseTag,
        pred: BaseTag = None
    ) -> None:
        assert isinstance(tp, BaseTag)

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
        pred: BaseTag = None
    ) -> BaseTag:
        tag = BaseTag(x)

        tag.SetObject(self)

        self.InsertTag(tag, pred)

        return tag
