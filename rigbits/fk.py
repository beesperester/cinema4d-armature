import c4d

from typing import Generator

from armature.modules.armature import ArmatureAdapter


def CreateCtrl(
    op: c4d.BaseObject
) -> Generator[ArmatureAdapter, None, None]:
    matrix = op.GetMg()

    Off = c4d.BaseObject(c4d.Onull)
    Off.SetName(
        op.GetName().replace("_Joint", "_Off")
    )
    Off.SetMg(matrix)

    Sdk = c4d.BaseObject(c4d.Onull)
    Sdk.SetName(
        op.GetName().replace("_Joint", "_Sdk")
    )
    Sdk.InsertUnder(Off)
    Sdk.SetMg(matrix)

    Ctrl = c4d.BaseObject(c4d.Onull)
    Ctrl.SetName(
        op.GetName().replace("_Joint", "_Ctrl")
    )
    Ctrl.InsertUnder(Sdk)
    Ctrl.SetMg(matrix)

    # derive tag name
    tag_name = op.GetName().replace("_Joint", "_Constraint")

    if tag_name not in [x.GetName() for x in op.GetTags()]:
        # add new constraint with tag name
        # if no tag with tag name exists
        constraint = op.MakeTag(c4d.Tconstraint)
        constraint.SetName(tag_name)

    # expose off adapter
    yield ArmatureAdapter("Off", Off)

    # expose ctrl adapter
    yield ArmatureAdapter("Ctrl", Ctrl)
