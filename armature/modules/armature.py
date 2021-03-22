from __future__ import annotations

import c4d

from collections import UserList
from typing import Generator, List, Optional, Union, Callable, Iterable

from armature.modules.hierarchy import Hierarchy


class ArmatureAdapter:
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
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__, self.GetName(), hex(id(self))
        )

    def GetName(self) -> str:
        return self._name

    def GetObject(self) -> c4d.BaseObject:
        return self._op

    def GetArmatureModule(self) -> Optional[ArmatureModule]:
        return self._armature_module


class ArmatureAdapters(UserList[ArmatureAdapter]):
    def __init__(
        self, adapters: Optional[List[ArmatureAdapter]] = None
    ) -> None:
        if adapters is None:
            adapters = List[ArmatureAdapter]()

        self.data = adapters

    def __getattr__(self, name: str) -> ArmatureAdapter:
        adapter_names = [x.GetName() for x in self.data]

        if name in adapter_names:
            return self.data[adapter_names.index(name)]

        raise AttributeError(
            "{} has no attribute '{}'".format(self.__class__.__name__, name)
        )


class ArmatureModules(UserList["ArmatureModule"]):
    def __init__(self, modules: Optional[List[ArmatureModule]] = None) -> None:
        if modules is None:
            modules = List[ArmatureModule]()

        self.data = modules

    def __getattr__(self, name: str) -> ArmatureModule:
        module_names = [x.GetName() for x in self.data]

        if name in module_names:
            return self.data[module_names.index(name)]

        raise AttributeError(
            "{} has no attribute '{}'".format(self.__class__.__name__, name)
        )


class ArmatureModule:
    def __init__(
        self,
        name: str,
        hierarchy: Hierarchy,
        adapters: ArmatureAdapters,
        parent: Optional[ArmatureModule] = None,
    ) -> None:
        self._name = name
        self._hierarchy = hierarchy
        self._modules = ArmatureModules()
        self._adapters = adapters
        self._parent = parent

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__, self.GetName(), hex(id(self))
        )

    def GetName(self) -> str:
        return self._name

    def GetHierarchy(self) -> Hierarchy:
        return self._hierarchy

    def GetModules(self) -> ArmatureModules:
        return self._modules

    def GetAdapters(self) -> ArmatureAdapters:
        return self._adapters

    def SetParent(self, parent: ArmatureModule) -> None:
        assert isinstance(parent, ArmatureModule)

        self._parent = parent

    def GetParent(self) -> Optional[ArmatureModule]:
        return self._parent

    def HasParent(self) -> bool:
        return self._parent is not None

    def Compose(self, modules: ArmatureModules):
        self._modules.extend(modules)

    def Setup(self) -> None:
        pass

    def Mount(self) -> None:
        # setup self
        self.Setup()

        # setup depending modules
        for module in self.GetModules():
            module.SetParent(self)
            module.Mount()


class Armature:
    def __init__(self, name: str, root: ArmatureModule) -> None:
        self._name = name
        self._root = root

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__, self.GetName(), hex(id(self))
        )

    def GetName(self) -> str:
        return self._name

    def GetRoot(self) -> ArmatureModule:
        return self._root

    def Mount(self) -> None:
        self._root.Mount()
