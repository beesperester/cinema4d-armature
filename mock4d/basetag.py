from __future__ import annotations

from typing import Optional

from mock4d import baselist2d
from mock4d import interfaces


class BaseTag(interfaces.IBaseTag, baselist2d.BaseList2D):
    """
    This class represents a Base Tag
    """

    def __init__(
        self,
        atom_type: int
    ):
        self._op: Optional[interfaces.IBaseObject] = None

        super(BaseTag, self).__init__(atom_type)

    def GetObject(self) -> Optional[interfaces.IBaseObject]:
        return self._op

    def SetObject(
        self,
        op: interfaces.IBaseObject
    ) -> None:
        self._op = op
