import c4d

from typing import Tuple

from examples.scene import Asset_Grp
from examples import asset, spine, leg

from rigging.utilities import iterator


asset_hierarchy = asset.shape.Extract(Asset_Grp)
spine_hierarchy = spine.shape.Extract(
    asset_hierarchy.rig.joints.root.pelvis.GetObject()
)

l_upperleg_hierarchy = leg.shape.Extract(
    spine_hierarchy.l_upperleg.GetObject()
)

l_upperleg_rig = leg.CreateRig(l_upperleg_hierarchy)

l_upperleg_off, _ = l_upperleg_rig.CreateCtrls()

print("ctrls")
for child in iterator.IterateHierarchy(l_upperleg_off):
    print(child)

print("\njoints")
for child in iterator.IterateHierarchy(l_upperleg_hierarchy.GetObject()):
    print(child, child.GetTags())