from mock4d.c4datom import C4DAtom
from mock4d.basecontainer import BaseContainer


class GeListNode(C4DAtom):
    """
    This class represents a Ge List Node
    """

    def __init__(
        self,
        atom_type: int
    ) -> None:
        self._children = []
        self._parent = None
        self._data = BaseContainer()

        super(GeListNode, self).__init__(atom_type)
    
    # def __setitem__(self, key, value):
    #     if not hasattr(self, key):
    #         self._data[key] = value
    
    # def __getitem__(self, key):
    #     if not hasattr(self, key):
    #         return self._data[key]
    
    def GetDown(self):
        if self._children:
            return self._children[0]
        
        return None
    
    def GetUp(self):
        return self._parent
    
    def GetChildren(self):
        return self._children
    
    def GetNext(self):
        if not self._parent:
            return None
        
        if not self._parent._children:
            return None
        
        own_index = self._parent._children.index(self)

        if own_index + 1 > len(self._parent._children) - 1:
            return None
        
        return self._parent._children[own_index + 1]
    
    def InsertUnder(self, parent):
        self._parent = parent

        if self not in self._parent._children:
            self._parent._children.append(self)