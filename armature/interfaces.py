import c4d

from typing import Optional, List

from armature.modules.hierarchy import Hierarchy


class INamed:
    def GetName(self) -> str:
        return ""


class IValidator:
    """
    This class represents a Validatorr Interface
    """

    def Validate(self, op: c4d.BaseObject) -> bool:
        raise NotImplementedError


class IShape:
    """
    This class represents a Shape Interface
    """

    def __init__(
        self, name: str, validators: Optional[List[IValidator]] = None
    ) -> None:
        raise NotImplementedError

    def GetValidators(self) -> List[IValidator]:
        raise NotImplementedError

    def GetName(self) -> str:
        raise NotImplementedError

    def Extract(self, op: c4d.BaseObject) -> Hierarchy:
        raise NotImplementedError
