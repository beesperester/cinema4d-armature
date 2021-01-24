import c4d

from typing import List, Union

from armature.modules.hierarchy import Hierarchy


class ArmatureAdapter:

    def __init__(
        self,
        name: str
    ) -> None:
        self._name = name
        self._op = None

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__,
            self.GetName(),
            hex(id(self))
        )

    @property
    def is_mounted(self) -> bool:
        return isinstance(self.GetObject(), c4d.BaseObject)

    def GetName(self) -> str:
        return self._name

    def SetObject(
        self,
        op: c4d.BaseObject
    ) -> None:
        assert isinstance(op, c4d.BaseObject)

        self._op = op

    def GetObject(self) -> c4d.BaseObject:
        return self._op


class Armature:

    def __init__(
        self,
        name: str,
        hierarchy: Hierarchy,
        modules: List["Armature"] = None,
        **kwargs
    ) -> None:
        if modules is None:
            modules = []

        self._name = name
        self._hierarchy = Hierarchy
        self._parent = None
        self._modules = [x.SetParent(self) for x in modules]
        self._adapters = []

        if "adapters" in kwargs.keys():
            self._adapters = kwargs["adapters"]

    def __repr__(self):
        return "<{} object '{}' at {}>".format(
            self.__class__.__name__,
            self.GetName(),
            hex(id(self))
        )

    def __getattr__(
        self,
        name: str
    ) -> Union["Armature", ArmatureAdapter]:
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

    @property
    def is_mounted(self) -> bool:
        return (
            all([x.is_mounted for x in self.GetAdapters()])
            if self.GetAdapters() else True
        )

    def GetName(self) -> str:
        return self._name

    def SetParent(
        self,
        parent: "Armature"
    ) -> "Armature":
        assert isinstance(parent, Armature)

        self._parent = parent

        return self

    def GetParent(self) -> "Armature":
        return self._parent

    def GetModules(self) -> List["Armature"]:
        return self._modules

    def GetAdapters(self) -> List[ArmatureAdapter]:
        return self._adapters

    def Mount(self) -> None:
        for adapter in self.GetAdapters():
            adapter.SetObject(c4d.BaseObject(c4d.Onull))


spine = Armature(
    "spine",
    "spine_hirarchy",
    [
        Armature(
            "l_leg",
            "l_leg_hierarchy"
        ),
        Armature(
            "r_leg",
            "r_leg_hierarchy"
        )
    ],
    adapters=[
        ArmatureAdapter("pelvis_ctrl"),
        ArmatureAdapter("chest_ctrl")
    ]
)

spine.Mount()

print(spine.module_l_leg.GetParent())

# import c4d

# from typing import Tuple

# from examples.scene import Asset_Grp
# from examples import asset, spine, leg

# from armature.utilities import iterator


# asset_hierarchy = asset.shape.Extract(Asset_Grp)
# spine_hierarchy = spine.shape.Extract(
#     asset_hierarchy.rig.joints.root.pelvis.GetObject()
# )

# l_upperleg_hierarchy = leg.shape.Extract(
#     spine_hierarchy.l_upperleg.GetObject()
# )

# l_upperleg_rig = leg.CreateRig(l_upperleg_hierarchy)

# l_upperleg_off, _ = l_upperleg_rig.CreateCtrls()

# print("ctrls")
# for child in iterator.IterateHierarchy(l_upperleg_off):
#     print(child)

# print("\njoints")
# for child in iterator.IterateHierarchy(l_upperleg_hierarchy.GetObject()):
#     print(child, child.GetTags())
