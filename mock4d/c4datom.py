class C4DAtom:
    """
    This class repersents a c4d Atom
    """

    def __init__(
        self,
        atom_type: int
    ) -> None:
        self._atom_type = atom_type
    
    def __repr__(self):
        return "<{}.{} object '{}'>".format(
            __name__,
            self.__class__.__name__,
            self.GetType()
        )
    
    def GetType(self):
        return self._atom_type