from __future__ import annotations

from typing import Optional

from mock4d import baselist2d, baseobject


class BaseTag(baselist2d.BaseList2D):
    """
    This class represents a Base Tag
    """

    def __init__(
        self,
        atom_type: int
    ):
        self._op: Optional[baseobject.BaseObject] = None

        super(BaseTag, self).__init__(atom_type)

    def GetObject(self) -> Optional[baseobject.BaseObject]:
        return self._op

    def SetObject(
        self,
        op: baseobject.BaseObject
    ) -> None:
        self._op = op
