from typing import Optional, Dict, Any, List

from mock4d import symbols


class C4DAtom:
    """
    This class repersents a c4d Atom
    """

    def __init__(
        self,
        atom_type: Optional[int] = None
    ) -> None:
        self._atom_name: Optional[str] = None

        variables: Dict[str, Any] = symbols.__dict__

        keys: List[str] = list(variables.keys())
        values: List[Any] = list(variables.values())

        if atom_type in values:
            self._atom_name = keys[values.index(atom_type)]

        self._atom_type = atom_type

    def __repr__(self) -> str:
        return "<{}.{} {} with id '{}' at {}>".format(
            __name__,
            self.__class__.__name__,
            self._atom_name,
            self.GetType(),
            hex(id(self))
        )

    def GetType(self) -> Optional[int]:
        return self._atom_type

    def GetTypeName(self) -> Optional[str]:
        return self._atom_name

    def CheckType(
        self,
        atom_type: int
    ) -> bool:
        return self.IsInstanceOf(atom_type)

    def IsInstanceOf(
        self,
        atom_type: int
    ) -> bool:
        return self.GetType() == atom_type
