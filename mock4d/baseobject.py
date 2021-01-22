from mock4d.baselist2d import BaseList2D


class BaseObject(BaseList2D):
    """
    This class represents a Base Object
    """

    def __init__(
        self,
        atom_type: int
    ):
        self._children = []
        self._parent = None

        super(BaseObject, self).__init__(atom_type)
    
    def GetDown(self):
        if self._children:
            return self._children[0]
        
        return None
    
    def GetUp(self):
        return self._parent
    
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
