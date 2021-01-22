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
        self._data = BaseContainer()

        super(BaseList2D, self).__init__(atom_type)
    
    def GetData(self):
        return copy.deepcopy(self.GetDataInstance())

    def GetDataInstance(self):
        return self._data
    
    def SetName(self, name):
        self._name = name

    def GetName(self):
        return self._name