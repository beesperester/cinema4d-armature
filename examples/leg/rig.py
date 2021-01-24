import c4d

from typing import Tuple

from armature.modules.rig import BaseRig

from examples.modules import fk


class Rig(BaseRig):


    def CreateCtrls(self) -> Tuple[c4d.BaseObject, c4d.BaseObject]:
        # create fk ctrls
        Upperleg_Off, Upperleg_Ctrl = fk.CreateCtrl(
            self.GetHierarchy().GetObject()
        )

        Lowerleg_Off, Lowerleg_Ctrl = fk.CreateCtrl(
            self.GetHierarchy().lowerleg.GetObject()
        )
        Lowerleg_Off.InsertUnder(Upperleg_Ctrl)

        Ankle_Off, Ankle_Ctrl = fk.CreateCtrl(
            self.GetHierarchy().lowerleg.ankle.GetObject()
        )
        Ankle_Off.InsertUnder(Lowerleg_Ctrl)

        return (Upperleg_Off, Ankle_Ctrl)
