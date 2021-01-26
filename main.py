from __future__ import annotations
from mock4d.symbols import Onull
from mock4d.baseobject import BaseObject

import c4d

from typing import List, Optional, Union, Callable, Generator

from armature.modules.hierarchy import Hierarchy
from armature.modules.armature import Armature, ArmatureAdapter

from examples.scene import Asset_Grp
from examples import leg, asset, spine


def CreateSpineCtrls(armature: Armature) -> Generator[ArmatureAdapter]:
    pelvis_ctrl_adapter = ArmatureAdapter(
        "pelvis_ctrl",
        c4d.BaseObject(c4d.Onull)
    )

    yield pelvis_ctrl_adapter


def CreateLegCtrls(armature: Armature) -> Generator[ArmatureAdapter]:
    leg_off_adapter = ArmatureAdapter(
        "l_leg_off",
        c4d.BaseObject(c4d.Onull)
    )

    print(armature.GetParent().adapter_pelvis_ctrl)

    yield leg_off_adapter


asset_hierarchy = asset.shape.Extract(Asset_Grp)
spine_hierarchy = spine.shape.Extract(
    asset_hierarchy.rig.joints.root.pelvis.GetObject()
)

l_leg_hierarchy = leg.shape.Extract(
    spine_hierarchy.l_upperleg.GetObject()
)


spine = Armature(
    "spine",
    spine_hierarchy,
    CreateSpineCtrls,
    [
        Armature(
            "l_leg",
            l_leg_hierarchy,
            CreateLegCtrls
        )
    ]
)

spine.Mount()
