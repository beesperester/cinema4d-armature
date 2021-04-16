import c4d
import unittest

from typing import List

from armature import dag, pieces


def create_example_baseobject():
    asset_object = c4d.BaseObject(c4d.Onull)
    asset_object.SetName("Asset_Grp")

    asset_constraint_tag = asset_object.MakeTag(1019364)  # type: ignore
    asset_constraint_tag.SetName("Asset_Constraint")

    rig_object = c4d.BaseObject(c4d.Onull)
    rig_object.SetName("Rig_Grp")
    rig_object.InsertUnder(asset_object)

    ctrls_object = c4d.BaseObject(c4d.Onull)
    ctrls_object.SetName("Ctrls_Grp")
    ctrls_object.InsertUnder(rig_object)

    joints_object = c4d.BaseObject(c4d.Onull)
    joints_object.SetName("Joints_Grp")
    joints_object.InsertUnder(rig_object)

    geo_object = c4d.BaseObject(c4d.Onull)
    geo_object.SetName("Geo_Grp")
    geo_object.InsertUnder(asset_object)

    return asset_object


def create_example_recursive_baseobject():
    spine_1_object = c4d.BaseObject(c4d.Ojoint)
    spine_1_object.SetName("Spine_1_Joint")

    spine_2_object = c4d.BaseObject(c4d.Ojoint)
    spine_2_object.SetName("Spine_2_Joint")
    spine_2_object.InsertUnder(spine_1_object)

    spine_3_object = c4d.BaseObject(c4d.Ojoint)
    spine_3_object.SetName("Spine_3_Joint")
    spine_3_object.InsertUnder(spine_2_object)

    spine_4_object = c4d.BaseObject(c4d.Ojoint)
    spine_4_object.SetName("Spine_4_Joint")
    spine_4_object.InsertUnder(spine_3_object)

    return spine_1_object


def create_example_dagatom():
    return dag.DagAtom(create_example_baseobject())


def create_example_recursive_dagbaselist2d():
    return dag.DagAtom(create_example_recursive_baseobject())


def create_example_dagbaseobject():
    return dag.DagBaseObject(create_example_baseobject())


def create_example_recursive_dagbaseobject():
    return dag.DagBaseObject(create_example_recursive_baseobject())


def create_example_baseobjects_list():
    base_objects_list: List[c4d.BaseObject] = []

    for i in range(0, 10):
        base_object = c4d.BaseObject(c4d.Onull)
        base_object.SetName("BaseObject_{}_Null".format(i + 1))

        base_objects_list.append(base_object)

    return base_objects_list


def create_example_daglist():
    return dag.DagAtomList(
        [dag.DagAtom(x) for x in create_example_baseobjects_list()]
    )


def create_example_dagbaseobjectlist():
    return dag.DagAtomList(
        [dag.DagBaseObject(x) for x in create_example_baseobjects_list()]
    )


def create_example_basetag():
    base_tag = c4d.BaseTag(1019364)
    base_tag.SetName("Constraint")

    return base_tag


def create_example_dagbasetag():
    return dag.DagBaseTag(create_example_basetag())


def create_example_basetags_list():
    base_tags_list: List[c4d.BaseTag] = []

    for i in range(1, 10):
        base_tag = c4d.BaseTag(1019364)
        base_tag.SetName("BaseTag_{}_Constraint".format(i))

        base_tags_list.append(base_tag)

    return base_tags_list


def create_example_dagbasetaglist():
    return dag.DagAtomList(
        [dag.DagBaseTag(x) for x in create_example_basetags_list()]
    )


def create_example_armaturemodule():
    spine_object = create_example_recursive_dagbaseobject()

    adapters = dag.DagBaseObjectList()

    spine_module = pieces.ArmatureModule(spine_object, adapters)

    return spine_module
