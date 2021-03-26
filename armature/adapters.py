from __future__ import annotations

import c4d
import logging

from collections import UserList
from typing import Generator, List, Optional, Union, Callable, Iterable

from armature.hierarchy import Hierarchy
from armature.modules import ArmatureModule
from armature.extensions.list import AcessibleList
from armature.interfaces import INamed


class ArmatureAdapter(INamed):
    def __init__(
        self,
        name: str,
        op: c4d.BaseObject,
        armature_module: ArmatureModule,
    ) -> None:
        self._name = name
        self._op = op
        self._armature_module = armature_module

    def __repr__(self):
        return "<{} object '{}::{}' at {}>".format(
            self.__class__.__name__,
            self.GetName(),
            self.GetArmatureModule().GetName(),
            hex(id(self)),
        )

    def GetName(self) -> str:
        return self._name

    def GetObject(self) -> c4d.BaseObject:
        return self._op

    def GetArmatureModule(self) -> Optional[ArmatureModule]:
        return self._armature_module


class ArmatureAdapters(AcessibleList[ArmatureAdapter]):
    """Acessible list of armature adapters"""
