class BaseObject:
    """
    This class represents a Base Object
    """

    def __init__(self):
        self._name = ""
        self._children = []
        self._parent = None
        self._data = {}
    
    def __repr__(self):
        return "<{}.{} object '{}'>".format(
            __name__,
            self.__class__.__name__,
            self.GetName()
        )

    def GetDataInstance(self):
        return self._data
    
    def SetName(self, name):
        self._name = name

    def GetName(self):
        return self._name
    
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


class NullObject(BaseObject):
    """
    This class represents a Null Object
    """


class JointObject(BaseObject):
    """
    This class represents a Joint Object
    """
