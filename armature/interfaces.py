import c4d

from typing import Optional, List

from armature import dag


class IValidator:
    """
    This class represents a Validatorr Interface
    """

    def GetName(self) -> str:
        raise NotImplementedError

    def Validate(self, base_object: dag.DagObject) -> None:
        raise NotImplementedError


class IValidationRule:
    """
    This class represents a Validation Rule Interface
    """

    def Test(self, validator: IValidator, base_object: dag.DagObject) -> bool:
        raise NotImplementedError
