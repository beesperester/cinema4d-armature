import c4d

# asset
Asset_Grp = c4d.BaseObject(c4d.Onull)
Asset_Grp.SetName("Asset_Grp")

# rig
Rig_Grp = c4d.BaseObject(c4d.Onull)
Rig_Grp.SetName("Rig_Grp")
Rig_Grp.InsertUnder(Asset_Grp)

# geometry
Geo_Grp = c4d.BaseObject(c4d.Onull)
Geo_Grp.SetName("Geo_Grp")
Geo_Grp.InsertUnder(Asset_Grp)

# ctrls
Ctrls_Grp = c4d.BaseObject(c4d.Onull)
Ctrls_Grp.SetName("Ctrls_Grp")
Ctrls_Grp.InsertUnder(Rig_Grp)

# joints
Joints_Grp = c4d.BaseObject(c4d.Onull)
Joints_Grp.SetName("Joints_Grp")
Joints_Grp.InsertUnder(Rig_Grp)

# root
Root_Joint = c4d.BaseObject(c4d.Ojoint)
Root_Joint.SetName("Root_Joint")
Root_Joint.InsertUnder(Joints_Grp)

# spine
Pelvis_Joint = c4d.BaseObject(c4d.Ojoint)
Pelvis_Joint.SetName("Pelvis_Joint")
Pelvis_Joint.InsertUnder(Root_Joint)

Spine_01_Joint = c4d.BaseObject(c4d.Ojoint)
Spine_01_Joint.SetName("Spine_01_Joint")
Spine_01_Joint.InsertUnder(Pelvis_Joint)

Spine_02_Joint = c4d.BaseObject(c4d.Ojoint)
Spine_02_Joint.SetName("Spine_02_Joint")
Spine_02_Joint.InsertUnder(Spine_01_Joint)

Spine_03_Joint = c4d.BaseObject(c4d.Ojoint)
Spine_03_Joint.SetName("Spine_03_Joint")
Spine_03_Joint.InsertUnder(Spine_02_Joint)

# l_leg
L_Upperleg_Joint = c4d.BaseObject(c4d.Ojoint)
L_Upperleg_Joint.SetName("L_Upperleg_Joint")
L_Upperleg_Joint.InsertUnder(Pelvis_Joint)

L_UpperlegWeight_Joint = c4d.BaseObject(c4d.Ojoint)
L_UpperlegWeight_Joint.SetName("L_UpperlegWeight_Joint")
L_UpperlegWeight_Joint.InsertUnder(L_Upperleg_Joint)

L_Lowerleg_Joint = c4d.BaseObject(c4d.Ojoint)
L_Lowerleg_Joint.SetName("L_Lowerleg_Joint")
L_Lowerleg_Joint.InsertUnder(L_Upperleg_Joint)

L_LowerlegWeight_Joint = c4d.BaseObject(c4d.Ojoint)
L_LowerlegWeight_Joint.SetName("L_LowerlegWeight_Joint")
L_LowerlegWeight_Joint.InsertUnder(L_Lowerleg_Joint)

L_Ankle_Joint = c4d.BaseObject(c4d.Ojoint)
L_Ankle_Joint.SetName("L_Ankle_Joint")
L_Ankle_Joint.InsertUnder(L_Lowerleg_Joint)

L_AnkleWeight_Joint = c4d.BaseObject(c4d.Ojoint)
L_AnkleWeight_Joint.SetName("L_AnkleWeight_Joint")
L_AnkleWeight_Joint.InsertUnder(L_Ankle_Joint)

L_Ball_Joint = c4d.BaseObject(c4d.Ojoint)
L_Ball_Joint.SetName("L_Ball_Joint")
L_Ball_Joint.InsertUnder(L_Ankle_Joint)

L_BallWeight_Joint = c4d.BaseObject(c4d.Ojoint)
L_BallWeight_Joint.SetName("L_BallWeight_Joint")
L_BallWeight_Joint.InsertUnder(L_Ball_Joint)