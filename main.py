import c4d

from typing import Tuple

from examples.scene import Asset_Grp, Root_Joint
from examples.asset_shape import asset_shape
from examples.root_shape import root_shape

asset_hierarchy = asset_shape.Exctract(Asset_Grp)
root_hierarchy = root_shape.Exctract(Root_Joint)

def CreateCtrl(
    op: c4d.BaseObject
) -> Tuple[c4d.BaseObject, c4d.BaseObject]:
    Off = c4d.BaseObject(c4d.Onull)
    Off.SetName(
        op.GetName().replace("_Joint", "_Off")
    )

    Sdk = c4d.BaseObject(c4d.Onull)
    Sdk.SetName(
        op.GetName().replace("_Joint", "_Sdk")
    )
    Sdk.InsertUnder(Off)

    Ctrl = c4d.BaseObject(c4d.Onull)
    Ctrl.SetName(
        op.GetName().replace("_Joint", "_Ctrl")
    )
    Ctrl.InsertUnder(Sdk)

    tag_name = op.GetName().replace("_Joint", "_Constraint")

    if not tag_name in [x.GetName() for x in op.GetTags()]:
        constraint = op.MakeTag(c4d.Tconstraint)
        constraint.SetName(tag_name)

    return (Off, Ctrl)

Root_Off, Root_Ctrl = CreateCtrl(root_hierarchy.GetObject())

print(Root_Off)