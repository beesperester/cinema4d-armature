from __future__ import annotations

from typing import TYPE_CHECKING

from mock4d.baselist2d import BaseList2D

if TYPE_CHECKING:
    from mock4d.baseobject import BaseObject


class BaseTag(BaseList2D):
    """
    This class represents a Base Tag
    """

    def __init__(
        self,
        atom_type: int
    ):
        self._op = None

        super(BaseTag, self).__init__(atom_type)
    
    def GetObject(self) -> BaseObject:
        return self._op
    
    def SetObject(
        self,
        op: BaseObject
    ) -> None:
        self._op = op
