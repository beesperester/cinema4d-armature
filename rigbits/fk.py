import c4d

from typing import Generator

from armature.modules.armature import ArmatureAdapter


def CreateCtrl(
    op: c4d.BaseObject
) -> Generator[ArmatureAdapter, None, None]:
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

    if tag_name not in [x.GetName() for x in op.GetTags()]:
        constraint = op.MakeTag(c4d.Tconstraint)
        constraint.SetName(tag_name)

    yield ArmatureAdapter("Off", Off)

    yield ArmatureAdapter("Ctrl", Ctrl)
