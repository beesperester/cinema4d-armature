from __future__ import annotations

import c4d

from typing import Generator, List, Optional, Union, Callable

from armature.modules.hierarchy import Hierarchy


class ArmatureAdapter:
    def __init__(
        self,
        name: str,
        op: c4d.BaseObject,
        armature: Optional[Armature] = None,
    ) -> None:
        self._name = name
        self._op = op
        self._armature = armature

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__, self.GetName(), hex(id(self))
        )

    def HasArmature(self) -> bool:
        return bool(self._armature)

    def GetName(self) -> str:
        return self._name

    def GetObject(self) -> c4d.BaseObject:
        return self._op

    def GetArmature(self) -> Optional[Armature]:
        return self._armature

    def SetArmature(self, armature: Armature) -> None:
        assert isinstance(armature, Armature)

        self._armature = armature


class ArmatureAdapters(List[ArmatureAdapter]):
    def __getattr__(self, name: str) -> ArmatureAdapter:
        adapter_names = [x.GetName() for x in self]

        if name in adapter_names:
            return self[adapter_names.index(name)]

        raise AttributeError(
            "{} has no attribute '{}'".format(self.__class__.__name__, name)
        )


class ArmatureModules(List["Armature"]):
    def __getattr__(self, name: str) -> Armature:
        module_names = [x.GetName() for x in self]

        if name in module_names:
            return self[module_names.index(name)]

        raise AttributeError(
            "{} has no attribute '{}'".format(self.__class__.__name__, name)
        )


class Armature:
    def __init__(
        self,
        name: str,
        hierarchy: Hierarchy,
        mount_callback: Callable[[Armature], None],
        adapters: Optional[ArmatureAdapters] = None,
        modules: Optional[ArmatureModules] = None,
    ) -> None:
        if adapters is None:
            adapters = ArmatureAdapters()

        if modules is None:
            modules = ArmatureModules()

        self._name = name
        self._hierarchy = hierarchy
        self._mount_callback = mount_callback
        self._parent = None

        self.SetAdapters(adapters)
        self.SetModules(modules)

        for module in modules:
            module.SetParent(self)

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__, self.GetName(), hex(id(self))
        )

    def GetAdapters(self) -> ArmatureAdapters:
        return self._adapters

    def SetAdapters(self, adapters: ArmatureAdapters) -> None:
        assert isinstance(adapters, ArmatureAdapters)

        self._adapters = adapters

    def GetModules(self) -> ArmatureModules:
        return self._modules

    def SetModules(self, modules: ArmatureModules) -> None:
        assert isinstance(modules, ArmatureModules)

        self._modules = modules

    def GetName(self) -> str:
        return self._name

    def GetHierarchy(self) -> Hierarchy:
        return self._hierarchy

    def SetParent(self, parent: Armature) -> None:
        assert isinstance(parent, Armature)

        self._parent = parent

    def GetParent(self) -> Optional[Armature]:
        return self._parent

    def Mount(self) -> None:
        self._mount_callback(self)

        # for adapter in self._mount_callback(self):
        #     adapter.SetArmature(self)

        #     self.GetAdapters().append(adapter)

        for module in self.GetModules():
            module.Mount()
