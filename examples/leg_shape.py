import c4d

from rigging.modules.shape import ObjectShape
from rigging.modules.shape.validators import (
    NameValidator,
    InstanceValidator
)

leg_shape = ObjectShape(
    "upperleg",
    [
        NameValidator("*_Upperleg_*"),
        InstanceValidator(c4d.JointObject)
    ],
    [
        ObjectShape(
            "weight",
            [
                NameValidator("*_UpperlegWeight_*"),
                InstanceValidator(c4d.JointObject)
            ]
        ),
        ObjectShape(
            "lowerleg",
            [
                NameValidator("*_Lowerleg_*"),
                InstanceValidator(c4d.JointObject)
            ],
            [
                ObjectShape(
                    "weight",
                    [
                        NameValidator("*_LowerlegWeight_*"),
                        InstanceValidator(c4d.JointObject)
                    ]
                ),
                ObjectShape(
                    "ankle",
                    [
                        NameValidator("*_Ankle_*"),
                        InstanceValidator(c4d.JointObject)
                    ]
                )
            ]
        )
    ]
)