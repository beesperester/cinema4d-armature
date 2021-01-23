import copy

from mock4d.gelistnode import GeListNode
from mock4d.basecontainer import BaseContainer


class BaseList2D(GeListNode):
    """
    This class represents a Base List 2D
    """    

    def __init__(
        self,
        atom_type: int
    ) -> None:
        self._name = ""

        super(BaseList2D, self).__init__(atom_type)
    
    def __repr__(self) -> str:
        object_name = "{}/{}".format(
            self.GetTypeName(),
            self.GetName()
        )

        return "<{} {} with id '{}' at {}>".format(
            self.__class__.__name__,
            object_name,
            self.GetType(),
            hex(id(self))
        )
    
    def GetData(self) -> BaseContainer:
        return copy.deepcopy(self.GetDataInstance())

    def GetDataInstance(self) -> BaseContainer:
        return self._data
    
    def SetName(self, name: str):
        assert isinstance(name, str)

        self._name = name

    def GetName(self) -> str:
        return self._name