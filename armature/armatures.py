from __future__ import annotations

from armature.interfaces import INamed
from armature.modules import ArmatureModule


class Armature(INamed):
    def __init__(self, name: str, root: ArmatureModule) -> None:
        self._name = name
        self._root = root

    def GetName(self) -> str:
        return self._name

    def GetRoot(self) -> ArmatureModule:
        return self._root

    def Mount(self) -> None:
        self._root.Mount()
