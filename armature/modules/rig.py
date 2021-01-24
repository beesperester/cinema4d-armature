from armature.modules.hierarchy import Hierarchy


class BaseRig:
    """
    This class represents a Base Rig
    """

    def __init__(
        self,
        hierarchy: Hierarchy
    ) -> None:
        self._hierarchy = hierarchy

    def GetHierarchy(self) -> Hierarchy:
        return self._hierarchy

    def CreateCtrls(self):
        raise NotImplementedError(
            "{} must implement 'CreateCtrls'".format(
                self.__class__.__name__
            )
        )
