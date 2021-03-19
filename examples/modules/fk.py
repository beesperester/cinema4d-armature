import c4d

from typing import Tuple


def CreateCtrl(op: c4d.BaseObject) -> Tuple[c4d.BaseObject, c4d.BaseObject]:
    Off = c4d.BaseObject(c4d.Onull)
    Off.SetName(op.GetName().replace("_Joint", "_Off"))  # type: ignore

    Sdk = c4d.BaseObject(c4d.Onull)
    Sdk.SetName(op.GetName().replace("_Joint", "_Sdk"))  # type: ignore
    Sdk.InsertUnder(Off)

    Ctrl = c4d.BaseObject(c4d.Onull)
    Ctrl.SetName(op.GetName().replace("_Joint", "_Ctrl"))  # type: ignore
    Ctrl.InsertUnder(Sdk)

    tag_name = op.GetName().replace("_Joint", "_Constraint")  # type: ignore

    if tag_name not in [x.GetName() for x in op.GetTags()]:  # type: ignore
        constraint = op.MakeTag(c4d.Tconstraint)  # type: ignore
        constraint.SetName(tag_name)

    return (Off, Ctrl)
