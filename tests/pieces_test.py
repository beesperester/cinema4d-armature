from typing import Generator
import c4d
import unittest

from armature import pieces, dag
from tests import utilities


class TestArmatureModule(unittest.TestCase):
    def test___init__(self):
        spine_module = utilities.create_example_armaturemodule()

        # assert instance of dagobject
        self.assertIsInstance(spine_module.GetDagObject(), dag.DagBaseObject)

        # assert instance of adapters
        self.assertIsInstance(
            spine_module.GetAdapters(), dag.DagBaseObjectList
        )

        # assert instance of object effects
        self.assertIsInstance(
            spine_module.GetObjecEffects(), dag.DagBaseObjectList
        )

        # assert instance of tag effects
        self.assertIsInstance(spine_module.GetTagEffects(), dag.DagBaseTagList)

    def test_CaptureEffects(self):
        spine_module = utilities.create_example_armaturemodule()

        def create_effects() -> Generator[dag.DagAtom, None, None]:
            ctrl_object = c4d.BaseObject(c4d.Onull)
            ctrl_object.SetName("Spine_1_Ctrl")

            # yield example DagBaseObject
            yield dag.DagBaseObject(ctrl_object)

            constraint_tag = c4d.BaseTag(1019364)
            constraint_tag.SetName("Constraint")

            # yield example DagBaseTag
            yield dag.DagBaseTag(constraint_tag)

        spine_module.CaptureEffects(create_effects())

        # assert adapters
        adapters_result = [x.GetName() for x in spine_module.GetAdapters()]
        adapters_result_expected = ["Spine_1_Ctrl"]

        self.assertListEqual(adapters_result, adapters_result_expected)

        # assert object effets
        object_effects_result = [
            x.GetName() for x in spine_module.GetObjecEffects()
        ]
        object_effects_result_expected = ["Spine_1_Ctrl"]

        self.assertListEqual(
            object_effects_result, object_effects_result_expected
        )

        # assert tag effects
        tag_effects_result = [
            x.GetName() for x in spine_module.GetTagEffects()
        ]
        tag_effects_result_expected = ["Constraint"]

        self.assertListEqual(tag_effects_result, tag_effects_result_expected)

    def test_Mount_raises_NotImplementedError(self):
        spine_module = utilities.create_example_armaturemodule()

        with self.assertRaises(NotImplementedError):
            spine_module.Mount()

    def test__TearDown(self):
        spine_module = utilities.create_example_armaturemodule()

        def create_effects() -> Generator[dag.DagAtom, None, None]:
            ctrl_object = c4d.BaseObject(c4d.Onull)
            ctrl_object.SetName("Spine_1_Ctrl")

            # yield example DagBaseObject
            yield dag.DagBaseObject(ctrl_object)

            constraint_tag = c4d.BaseTag(1019364)
            constraint_tag.SetName("Constraint")

            # yield example DagBaseTag
            yield dag.DagBaseTag(constraint_tag)

        spine_module.CaptureEffects(create_effects())

        spine_module._TearDown()

        # assert adapters
        adapters_result = [x.GetName() for x in spine_module.GetAdapters()]
        adapters_result_expected = []

        self.assertListEqual(adapters_result, adapters_result_expected)

        # assert object effets
        object_effects_result = [
            x.GetName() for x in spine_module.GetObjecEffects()
        ]
        object_effects_result_expected = []

        self.assertListEqual(
            object_effects_result, object_effects_result_expected
        )

        # assert tag effects
        tag_effects_result = [
            x.GetName() for x in spine_module.GetTagEffects()
        ]
        tag_effects_result_expected = []

        self.assertListEqual(tag_effects_result, tag_effects_result_expected)


if __name__ == "__main__":
    unittest.main()
