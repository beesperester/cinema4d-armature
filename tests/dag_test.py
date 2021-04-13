import c4d
import unittest

from typing import List

from armature import dag


def create_example_base_object():
    asset_object = c4d.BaseObject(c4d.Onull)
    asset_object.SetName("Asset_Grp")

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
    return dag.DagBaseList2D(create_example_base_object())


def create_example_base_objects_list():
    base_objects_list: List[c4d.BaseObject] = []

    for i in range(0, 10):
        base_object = c4d.BaseObject(c4d.Onull)
        base_object.SetName("BaseObject_{}_Null".format(i + 1))

        base_objects_list.append(base_object)

    return base_objects_list


def create_example_dagbaselist2dlist():
    return dag.DagBaseList2DList(create_example_base_objects_list())


class TestDagModuleDagBaseList2D(unittest.TestCase):
    def test_GetName(self):
        asset_object = create_example_dagbaselist2d()

        # assert resulting name
        result = asset_object.GetName()
        result_expected = "Asset_Grp"

        self.assertEqual(result, result_expected)

    def test_GetType(self):
        asset_object = create_example_dagbaselist2d()

        # assert resulting type
        result = asset_object.GetType()
        result_expected = c4d.Onull

        self.assertEqual(result, result_expected)

    def test_GetChildren(self):
        asset_object = create_example_dagbaselist2d()

        # assert resulting instance
        self.assertIsInstance(
            asset_object.GetChildren(), dag.DagBaseList2DList
        )

        # assert list of resulting names
        result = [x.GetName() for x in asset_object.GetChildren()]
        result_expected = ["Geo_Grp", "Rig_Grp"]

        self.assertListEqual(result, result_expected)

    def test_GetChild(self):
        asset_object = create_example_dagbaselist2d()

        child = asset_object.GetChild("Geo_Grp")

        # assert resulting instance
        self.assertIsInstance(child, dag.DagBaseList2D)

        # assert name of resulting child
        result = child.GetName()
        result_expected = "Geo_Grp"

        self.assertEqual(result, result_expected)


class TestDagModuleDagBaseList2DList(unittest.TestCase):
    def test___iter__(self):
        example_list = create_example_dagbaselist2dlist()

        result = []

        for item in example_list:
            result.append(item.GetName())

        result_expected = [
            "BaseObject_{}_Null".format(x + 1) for x in range(0, 10)
        ]

        self.assertListEqual(result, result_expected)

    def test___getitem__(self):
        example_list = create_example_dagbaselist2dlist()

        result = example_list[0].GetName()
        result_expected = "BaseObject_1_Null"

        self.assertEqual(result, result_expected)

    def test_Get(self):
        example_list = create_example_dagbaselist2dlist()

        item = example_list.Get("BaseObject_2_Null")

        # assert resulting instance
        self.assertIsInstance(item, dag.DagBaseList2D)

        # assert resulting name
        result = item.GetName()
        result_expected = "BaseObject_2_Null"

        self.assertEqual(result, result_expected)

    def test_Get_raise_DagNotFoundError(self):
        example_list = create_example_dagbaselist2dlist()

        with self.assertRaises(dag.DagNotFoundError):
            example_list.Get("YouCanNotFindMe")

    def test_Extend(self):
        example_list = create_example_dagbaselist2dlist()

        new_object = c4d.BaseList2D(c4d.Onull)
        new_object.SetName("NewItem_Null")

        new_list = dag.DagBaseList2DList([new_object])

        example_list.Extend(new_list)

        result = example_list.Get("NewItem_Null").GetName()
        result_expected = "NewItem_Null"

        self.assertEqual(result, result_expected)

    def testAppend(self):
        example_list = create_example_dagbaselist2dlist()

        new_object = c4d.BaseList2D(c4d.Onull)
        new_object.SetName("NewItem_Null")

        example_list.Append(dag.DagBaseList2D(new_object))

        result = example_list.Get("NewItem_Null").GetName()
        result_expected = "NewItem_Null"

        self.assertEqual(result, result_expected)


if __name__ == "__main__":
    unittest.main()
