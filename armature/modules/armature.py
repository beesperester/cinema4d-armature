from __future__ import annotations

import c4d

from typing import Generator, List, Optional, Union, Callable

from armature.modules.hierarchy import Hierarchy


class ArmatureAdapter:

    def __init__(
        self,
        name: str,
        op: c4d.BaseObject
    ) -> None:
        self._name = name
        self._op = op

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__,
            self.GetName(),
            hex(id(self))
        )

    def GetName(self) -> str:
        return self._name

    def GetObject(self) -> c4d.BaseObject:
        return self._op


class Armature:

    def __init__(
        self,
        name: str,
        hierarchy: Hierarchy,
        mount_callback: Callable[[Armature], Generator[ArmatureAdapter]],
        modules: Optional[List[Armature]] = None
    ) -> None:
        if modules is None:
            modules = []

        for module in modules:
            module.SetParent(self)

        self._name = name
        self._hierarchy = Hierarchy
        self._mount_callback = mount_callback
        self._parent = None
        self._modules = modules
        self._adapters = []

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__,
            self.GetName(),
            hex(id(self))
        )

    def __getattr__(
        self,
        name: str
    ) -> Union[Armature, ArmatureAdapter]:
        if name.startswith("adapter_"):
            name = name.replace("adapter_", "")

            adapter_names = [x.GetName() for x in self.GetAdapters()]

            if name in adapter_names:
                return self.GetAdapters()[adapter_names.index(name)]

        if name.startswith("module_"):
            name = name.replace("module_", "")

            module_names = [x.GetName() for x in self.GetModules()]

            if name in module_names:
                return self.GetModules()[module_names.index(name)]

        raise AttributeError(
            "{} has no attribute '{}'".format(
                self.__class__.__name__,
                name
            )
        )

    def GetName(self) -> str:
        return self._name

    def SetParent(
        self,
        parent: Armature
    ) -> None:
        assert isinstance(parent, Armature)

        self._parent = parent

    def GetParent(self) -> Optional[Armature]:
        return self._parent

    def GetModules(self) -> List[Armature]:
        return self._modules

    def GetAdapters(self) -> List[ArmatureAdapter]:
        return self._adapters

    def Mount(self) -> None:
        for adapter in self._mount_callback(self):
            self._adapters.append(adapter)

        for module in self.GetModules():
            module.Mount()
