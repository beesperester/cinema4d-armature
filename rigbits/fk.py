import c4d

from typing import Generator, List

from armature.modules.armature import ArmatureAdapter


def CreateCtrl(op: c4d.BaseObject) -> Generator[ArmatureAdapter, None, None]:
    matrix = op.GetMg()

    Off = c4d.BaseObject(c4d.Onull)
    Off.SetName(str(op.GetName()).replace("_Joint", "_Off"))
    Off.SetMg(matrix)

    Sdk = c4d.BaseObject(c4d.Onull)
    Sdk.SetName(str(op.GetName()).replace("_Joint", "_Sdk"))
    Sdk.InsertUnder(Off)
    Sdk.SetMg(matrix)

    Ctrl = c4d.BaseObject(c4d.Onull)
    Ctrl.SetName(str(op.GetName()).replace("_Joint", "_Ctrl"))
    Ctrl.InsertUnder(Sdk)
    Ctrl.SetMg(matrix)

    # derive tag name
    tag_name = str(op.GetName()).replace("_Joint", "_Constraint")

    op_tags: List[c4d.BaseTag] = op.GetTags()  # type: ignore
    tag_names: List[str] = [str(x.GetName()) for x in op_tags]

    if tag_name not in tag_names:
        # add new constraint with tag name
        # if no tag with tag name exists
        constraint: c4d.BaseTag = op.MakeTag(1019364)  # type: ignore
        constraint.SetName(tag_name)

    # expose off adapter
    yield ArmatureAdapter("Off", Off)

    # expose ctrl adapter
    yield ArmatureAdapter("Ctrl", Ctrl)
