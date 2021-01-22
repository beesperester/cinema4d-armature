import c4d
import logging

from rigging.modules.shape import ObjectShape
from rigging.modules.shape.validators import NameValidator, ChildrenValidator, InstanceValidator, ValidateAndRaise

logging.basicConfig(level=logging.ERROR)

asset_grp = c4d.NullObject()
asset_grp.SetName("Asset_Grp")

rig_grp = c4d.NullObject()
rig_grp.SetName("Rig_Grp")
rig_grp.InsertUnder(asset_grp)

joints_grp = c4d.NullObject()
joints_grp.SetName("Joints_Grp")
joints_grp.InsertUnder(rig_grp)

l_upperleg_joint = c4d.JointObject()
l_upperleg_joint.SetName("L_Upperleg_Joint")
l_upperleg_joint.InsertUnder(joints_grp)

test_joint = c4d.JointObject()
test_joint.SetName("Test_Joint")
test_joint.InsertUnder(l_upperleg_joint)

l_lowerleg_joint = c4d.JointObject()
l_lowerleg_joint.SetName("L_Lowerleg_Joint")
l_lowerleg_joint.InsertUnder(l_upperleg_joint)

l_ankle_joint = c4d.JointObject()
l_ankle_joint.SetName("L_Ankle_Joint")
l_ankle_joint.InsertUnder(l_lowerleg_joint)

l_ball_joint = c4d.JointObject()
l_ball_joint.SetName("L_Ball_Joint")
l_ball_joint.InsertUnder(l_ankle_joint)

ctrls_grp = c4d.NullObject()
ctrls_grp.SetName("Ctrls_Grp")
ctrls_grp.InsertUnder(rig_grp)

# for op in IterateHierarchy(asset_grp):
#     print(op)

leg_shape = ObjectShape(
    "upperleg",
    [
        NameValidator("*_Upperleg_*"),
        InstanceValidator(c4d.JointObject),
        ChildrenValidator([
            ObjectShape(
                "lowerleg",
                [
                    NameValidator("*_Lowerleg_*"),
                    InstanceValidator(c4d.JointObject),
                    ChildrenValidator([
                        ObjectShape(
                            "ankle",
                            [
                                NameValidator("*_Ankle_*"),
                                InstanceValidator(c4d.JointObject)
                            ]
                        )
                    ])
                ]
            )
        ])
    ]
)

ValidateAndRaise(l_upperleg_joint, leg_shape)

# hierarchy = GetHierarchy(l_upperleg_joint, leg_shape)