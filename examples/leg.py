import c4d

from typing import Tuple

from armature.modules.shape.shapes import ObjectShape
from armature.modules.shape.validators import (
    NameValidator,
    InstanceValidator
)

# from examples.modules import fk


# def CreateCtrls(self) -> Tuple[c4d.BaseObject, c4d.BaseObject]:
#     # create fk ctrls
#     Upperleg_Off, Upperleg_Ctrl = fk.CreateCtrl(
#         self.GetHierarchy().GetObject()
#     )

#     Lowerleg_Off, Lowerleg_Ctrl = fk.CreateCtrl(
#         self.GetHierarchy().lowerleg.GetObject()
#     )
#     Lowerleg_Off.InsertUnder(Upperleg_Ctrl)

#     Ankle_Off, Ankle_Ctrl = fk.CreateCtrl(
#         self.GetHierarchy().lowerleg.ankle.GetObject()
#     )
#     Ankle_Off.InsertUnder(Lowerleg_Ctrl)

#     return (Upperleg_Off, Ankle_Ctrl)


shape = ObjectShape(
    "upperleg",
    [
        NameValidator("*_Upperleg_*"),
        InstanceValidator(c4d.Ojoint)
    ],
    [
        ObjectShape(
            "weight",
            [
                NameValidator("*_UpperlegWeight_*"),
                InstanceValidator(c4d.Ojoint)
            ]
        ),
        ObjectShape(
            "lowerleg",
            [
                NameValidator("*_Lowerleg_*"),
                InstanceValidator(c4d.Ojoint)
            ],
            [
                ObjectShape(
                    "weight",
                    [
                        NameValidator("*_LowerlegWeight_*"),
                        InstanceValidator(c4d.Ojoint)
                    ]
                ),
                ObjectShape(
                    "ankle",
                    [
                        NameValidator("*_Ankle_*"),
                        InstanceValidator(c4d.Ojoint)
                    ]
                )
            ]
        )
    ]
)
