from __future__ import annotations

import c4d

from typing import Generator, List, Optional, Union, Callable

from armature.modules.hierarchy import Hierarchy


class ArmatureAdapter:
    def __init__(self, name: str, op: c4d.BaseObject) -> None:
        self._name = name
        self._op = op

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__, self.GetName(), hex(id(self))
        )

    def GetName(self) -> str:
        return self._name

    def GetObject(self) -> c4d.BaseObject:
        return self._op


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
        mount_callback: Callable[
            [Armature], Generator[ArmatureAdapter, None, None]
        ],
        modules: Optional[List[Armature]] = None,
    ) -> None:
        if modules is None:
            modules = []

        for module in modules:
            module.SetParent(self)

        self._name = name
        self._hierarchy = hierarchy
        self._mount_callback = mount_callback
        self._parent = None

        self.modules = ArmatureModules(modules)
        self.adapters = ArmatureAdapters()

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__, self.GetName(), hex(id(self))
        )

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
        for adapter in self._mount_callback(self):
            self.adapters.append(adapter)

        for module in self.modules:
            module.Mount()
