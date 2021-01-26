from armature.modules import shape
import c4d

from typing import Tuple

from armature.modules.shape.shapes import ObjectShape
from armature.modules.shape.validators import (
    NameValidator,
    InstanceValidator
)


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
