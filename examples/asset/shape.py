import c4d

from rigging.modules.shape import ObjectShape
from rigging.modules.shape.validators import (
    NameValidator,
    InstanceValidator
)

shape = ObjectShape(
    "asset",
    [
        NameValidator("Asset_Grp"),
        InstanceValidator(c4d.Onull)
    ],
    [
        ObjectShape(
            "rig",
            [
                NameValidator("Rig_Grp"),
                InstanceValidator(c4d.Onull)
            ],
            [
                ObjectShape(
                    "ctrls",
                    [
                        NameValidator("Ctrls_Grp"),
                        InstanceValidator(c4d.Onull)
                    ]
                ),
                ObjectShape(
                    "joints",
                    [
                        NameValidator("Joints_Grp"),
                        InstanceValidator(c4d.Onull)
                    ],
                    [
                        ObjectShape(
                            "root",
                            [
                                NameValidator("Root_Joint"),
                                InstanceValidator(c4d.Ojoint)
                            ],
                            [
                                ObjectShape(
                                    "pelvis",
                                    [
                                        NameValidator("Pelvis_Joint"),
                                        InstanceValidator(c4d.Ojoint)
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)