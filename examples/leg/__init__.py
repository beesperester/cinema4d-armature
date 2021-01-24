from rigging.modules.hierarchy import Hierarchy

from examples.leg.shape import shape
from examples.leg.rig import Rig

def CreateRig(hierarchy: Hierarchy) -> Rig:
    return Rig(hierarchy)