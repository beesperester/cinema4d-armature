from mock4d.c4datom import C4DAtom


class GeListNode(C4DAtom):
    """
    This class represents a Ge List Node
    """

    def __init__(
        self,
        atom_type: int
    ) -> None:
        self._data = {}

        super(GeListNode, self).__init__(atom_type)
    
    def __setitem__(self, key, value):
        if not hasattr(self, key):
            self._data[key] = value

        return super(GeListNode, self).__setitem__(key, value)
    
    def __getitem__(self, key):
        if not hasattr(self, key):
            return self._data[key]
        
        return super(GeListNode, self).__getitem__(key)