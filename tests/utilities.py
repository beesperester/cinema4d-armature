import c4d
import unittest

from typing import List

from armature import dag


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


def create_example_dagbaselist2d():
    return dag.DagBaseList2D(create_example_baseobject())


def create_example_dagbaseobject():
    return dag.DagBaseObject(create_example_baseobject())


def create_example_baseobjects_list():
    base_objects_list: List[c4d.BaseObject] = []

    for i in range(0, 10):
        base_object = c4d.BaseObject(c4d.Onull)
        base_object.SetName("BaseObject_{}_Null".format(i + 1))

        base_objects_list.append(base_object)

    return base_objects_list


def create_example_dagbaselist2dlist():
    return dag.DagBaseList2DList(create_example_baseobjects_list())


def create_example_dagbaseobjectlist():
    return dag.DagBaseObjectList(create_example_baseobjects_list())


def create_example_basetag():
    base_tag = c4d.BaseTag(1019364)
    base_tag.SetName("Constraint")

    return base_tag


def create_example_dagbasetag():
    return dag.DagBaseTag(create_example_basetag())


def create_example_basetags_list():
    base_tags_list: List[c4d.BaseTag] = []

    for i in range(0, 10):
        base_tag = c4d.BaseTag(1019364)
        base_tag.SetName("BaseTag_{}_Constraint".format(i + 1))

        base_tags_list.append(base_tag)

    return base_tags_list


def create_example_dagbasetaglist():
    return dag.DagBaseTagList(create_example_basetags_list())
