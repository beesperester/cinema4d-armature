import c4d
import unittest

from typing import List

from armature import dag
from tests import utilities


class TestDagBaseList2D(unittest.TestCase):
    def test_GetName(self):
        asset_object = utilities.create_example_dagbaselist2d()

        # assert resulting name
        result = asset_object.GetName()
        result_expected = "Asset_Grp"

        self.assertEqual(result, result_expected)

    def test_GetType(self):
        asset_object = utilities.create_example_dagbaselist2d()

        # assert resulting type
        result = asset_object.GetType()
        result_expected = c4d.Onull

        self.assertEqual(result, result_expected)

    def test_GetChildren(self):
        asset_object = utilities.create_example_dagbaselist2d()

        # assert resulting instance
        self.assertIsInstance(
            asset_object.GetChildren(), dag.DagBaseList2DList
        )

        # assert list of resulting names
        result = [x.GetName() for x in asset_object.GetChildren()]
        result_expected = ["Geo_Grp", "Rig_Grp"]

        self.assertListEqual(result, result_expected)

    def test_GetChild(self):
        asset_object = utilities.create_example_dagbaselist2d()

        child = asset_object.GetChild("Geo_Grp")

        # assert resulting instance
        self.assertIsInstance(child, dag.DagBaseList2D)

        # assert name of resulting child
        result = child.GetName()
        result_expected = "Geo_Grp"

        self.assertEqual(result, result_expected)

    def test_GetParent(self):
        asset_object = utilities.create_example_dagbaselist2d()

        child = asset_object.GetChild("Geo_Grp")

        parent = child.GetParent()

        # assert resulting instance
        self.assertIsInstance(parent, dag.DagBaseList2D)

        # assert name of resulting parent
        result = parent.GetName()
        result_expected = "Asset_Grp"

        self.assertEqual(result, result_expected)

    def test_GetRecursive(self):
        asset_object = utilities.create_example_recursive_dagbaselist2d()

        result = []

        for child in asset_object.GetRecursive("Spine_*_Grp"):
            # assert resulting instance
            self.assertIsInstance(child, dag.DagBaseList2D)

            result.append(child.GetName())

        result_expected = ["Spine_2_Grp", "Spine_3_Grp", "Spine_4_Grp"]

        self.assertListEqual(result, result_expected)


class TestDagBaseObject(unittest.TestCase):
    def test_GetChildren(self):
        asset_object = utilities.create_example_dagbaseobject()

        # assert resulting instance
        self.assertIsInstance(
            asset_object.GetChildren(), dag.DagBaseObjectList
        )

        # assert list of resulting names
        result = [x.GetName() for x in asset_object.GetChildren()]
        result_expected = ["Geo_Grp", "Rig_Grp"]

        self.assertListEqual(result, result_expected)

    def test_GetChild(self):
        asset_object = utilities.create_example_dagbaseobject()

        child = asset_object.GetChild("Geo_Grp")

        # assert resulting instance
        self.assertIsInstance(child, dag.DagBaseObject)

        # assert name of resulting child
        result = child.GetName()
        result_expected = "Geo_Grp"

        self.assertEqual(result, result_expected)

    def test_GetParent(self):
        asset_object = utilities.create_example_dagbaseobject()

        child = asset_object.GetChild("Geo_Grp")

        parent = child.GetParent()

        # assert resulting instance
        self.assertIsInstance(parent, dag.DagBaseObject)

        # assert name of resulting parent
        result = parent.GetName()
        result_expected = "Asset_Grp"

        self.assertEqual(result, result_expected)

    def test_GetTags(self):
        asset_object = utilities.create_example_dagbaseobject()

        tags = asset_object.GetTags()

        # assert resulting instance
        self.assertIsInstance(tags, dag.DagBaseTagList)

        # assert resulting names
        result = [x.GetName() for x in tags]
        result_excpected = ["Asset_Constraint"]

        self.assertListEqual(result, result_excpected)

    def test_GetTag(self):
        asset_object = utilities.create_example_dagbaseobject()

        tag = asset_object.GetTag("Asset_Constraint")

        # assert resulting instance
        self.assertIsInstance(tag, dag.DagBaseTag)

        # assert resulting name
        result = tag.GetName()
        result_expected = "Asset_Constraint"

        self.assertEqual(result, result_expected)

    def test_GetRecursive(self):
        asset_object = utilities.create_example_recursive_dagbaseobject()

        result = []

        for child in asset_object.GetRecursive("Spine_*_Grp"):
            # assert resulting instance
            self.assertIsInstance(child, dag.DagBaseObject)

            result.append(child.GetName())

        result_expected = ["Spine_2_Grp", "Spine_3_Grp", "Spine_4_Grp"]

        self.assertListEqual(result, result_expected)


class TestDagBaseList2DList(unittest.TestCase):
    def test___iter__(self):
        example_list = utilities.create_example_dagbaselist2dlist()

        result = []

        for item in example_list:
            result.append(item.GetName())

            # assert resulting instance
            self.assertIsInstance(item, dag.DagBaseList2D)

        result_expected = [
            "BaseObject_{}_Null".format(x + 1) for x in range(0, 10)
        ]

        self.assertListEqual(result, result_expected)

    def test___getitem__(self):
        example_list = utilities.create_example_dagbaselist2dlist()

        item = example_list[0]

        # assert resulting instance
        self.assertIsInstance(item, dag.DagBaseList2D)

        # assert resulting name
        result = item.GetName()
        result_expected = "BaseObject_1_Null"

        self.assertEqual(result, result_expected)

    def test_Get(self):
        example_list = utilities.create_example_dagbaselist2dlist()

        item = example_list.Get("BaseObject_2_Null")

        # assert resulting instance
        self.assertIsInstance(item, dag.DagBaseList2D)

        # assert resulting name
        result = item.GetName()
        result_expected = "BaseObject_2_Null"

        self.assertEqual(result, result_expected)

    def test_Get_raise_DagNotFoundError(self):
        example_list = utilities.create_example_dagbaselist2dlist()

        with self.assertRaises(dag.DagNotFoundError):
            example_list.Get("YouCanNotFindMe")

    def test_Extend(self):
        example_list = utilities.create_example_dagbaselist2dlist()

        new_object = c4d.BaseList2D(c4d.Onull)
        new_object.SetName("NewItem_Null")

        new_list = dag.DagBaseList2DList([new_object])

        example_list.Extend(new_list)

        result = example_list.Get("NewItem_Null").GetName()
        result_expected = "NewItem_Null"

        self.assertEqual(result, result_expected)

    def test_Append(self):
        example_list = utilities.create_example_dagbaselist2dlist()

        new_object = c4d.BaseList2D(c4d.Onull)
        new_object.SetName("NewItem_Null")

        example_list.Append(dag.DagBaseList2D(new_object))

        result = example_list.Get("NewItem_Null").GetName()
        result_expected = "NewItem_Null"

        self.assertEqual(result, result_expected)


class TestDagBaseObjectList(unittest.TestCase):
    def test___iter__(self):
        example_list = utilities.create_example_dagbaseobjectlist()

        result = []

        for item in example_list:
            result.append(item.GetName())

            # assert resulting instance
            self.assertIsInstance(item, dag.DagBaseObject)

        result_expected = [
            "BaseObject_{}_Null".format(x + 1) for x in range(0, 10)
        ]

        self.assertListEqual(result, result_expected)

    def test___getitem__(self):
        example_list = utilities.create_example_dagbaseobjectlist()

        item = example_list[0]

        # assert resulting instance
        self.assertIsInstance(item, dag.DagBaseObject)

        # assert resulting name
        result = item.GetName()
        result_expected = "BaseObject_1_Null"

        self.assertEqual(result, result_expected)

    def test_Get(self):
        example_list = utilities.create_example_dagbaseobjectlist()

        item = example_list.Get("BaseObject_2_Null")

        # assert resulting instance
        self.assertIsInstance(item, dag.DagBaseObject)

        # assert resulting name
        result = item.GetName()
        result_expected = "BaseObject_2_Null"

        self.assertEqual(result, result_expected)

    def test_Get_raise_DagNotFoundError(self):
        example_list = utilities.create_example_dagbaseobjectlist()

        with self.assertRaises(dag.DagNotFoundError):
            example_list.Get("YouCanNotFindMe")

    def test_Extend(self):
        example_list = utilities.create_example_dagbaseobjectlist()

        new_object = c4d.BaseObject(c4d.Onull)
        new_object.SetName("NewItem_Null")

        new_list = dag.DagBaseObjectList([new_object])

        example_list.Extend(new_list)

        result = example_list.Get("NewItem_Null").GetName()
        result_expected = "NewItem_Null"

        self.assertEqual(result, result_expected)

    def test_Append(self):
        example_list = utilities.create_example_dagbaseobjectlist()

        new_object = c4d.BaseObject(c4d.Onull)
        new_object.SetName("NewItem_Null")

        example_list.Append(dag.DagBaseObject(new_object))

        result = example_list.Get("NewItem_Null").GetName()
        result_expected = "NewItem_Null"

        self.assertEqual(result, result_expected)


class TestDagBaseTagList(unittest.TestCase):
    def test___iter__(self):
        example_list = utilities.create_example_dagbasetaglist()

        result = []

        for item in example_list:
            result.append(item.GetName())

            # assert resulting instance
            self.assertIsInstance(item, dag.DagBaseTag)

        result_expected = [
            "BaseTag_{}_Constraint".format(x + 1) for x in range(0, 10)
        ]

        self.assertListEqual(result, result_expected)

    def test___getitem__(self):
        example_list = utilities.create_example_dagbasetaglist()

        item = example_list[0]

        # assert resulting instance
        self.assertIsInstance(item, dag.DagBaseTag)

        # assert resulting name
        result = item.GetName()
        result_expected = "BaseTag_1_Constraint"

        self.assertEqual(result, result_expected)

    def test_Get(self):
        example_list = utilities.create_example_dagbasetaglist()

        item = example_list.Get("BaseTag_2_Constraint")

        # assert resulting instance
        self.assertIsInstance(item, dag.DagBaseTag)

        # assert resulting name
        result = item.GetName()
        result_expected = "BaseTag_2_Constraint"

        self.assertEqual(result, result_expected)

    def test_Get_raise_DagNotFoundError(self):
        example_list = utilities.create_example_dagbasetaglist()

        with self.assertRaises(dag.DagNotFoundError):
            example_list.Get("YouCanNotFindMe")

    def test_Extend(self):
        example_list = utilities.create_example_dagbasetaglist()

        new_object = c4d.BaseTag(1019364)
        new_object.SetName("NewItem_Constraint")

        new_list = dag.DagBaseTagList([new_object])

        example_list.Extend(new_list)

        result = example_list.Get("NewItem_Constraint").GetName()
        result_expected = "NewItem_Constraint"

        self.assertEqual(result, result_expected)

    def test_Append(self):
        example_list = utilities.create_example_dagbasetaglist()

        new_object = c4d.BaseTag(1019364)
        new_object.SetName("NewItem_Constraint")

        example_list.Append(dag.DagBaseTag(new_object))

        result = example_list.Get("NewItem_Constraint").GetName()
        result_expected = "NewItem_Constraint"

        self.assertEqual(result, result_expected)


if __name__ == "__main__":
    unittest.main()
