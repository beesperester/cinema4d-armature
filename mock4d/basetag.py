from mock4d.baselist2d import BaseList2D


class BaseTag(BaseList2D):
    """
    This class represents a Base Object
    """

    def __new__(
        cls,
        type: int
    ) -> "BaseTag":
        pass

    def __init__(
        self,
        type: int
    ):
        self._type = type
        self._op = None
    
    def GetObject(self):
        return self._op
