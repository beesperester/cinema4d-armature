from tests import utilities
import c4d
import unittest

from typing import List
from beutils import dictutils, exceptions

from armature import serialize


class TestSerializeModule(unittest.TestCase):
    def test_serialize_vector_as_dict(self):
        vector = c4d.Vector()

        result = serialize.serialize_vector_as_dict(vector)
        result_expected = {"instance_of": "c4d.Vector", "x": 0, "y": 0, "z": 0}

        self.assertDictEqual(result, result_expected)

    def test_serialize_matrix_as_dict(self):
        matrix = c4d.Matrix()

        result = serialize.serialize_matrix_as_dict(matrix)
        result_expected = {
            "instance_of": "c4d.Matrix",
            "off": {"instance_of": "c4d.Vector", "x": 0, "y": 0, "z": 0},
            "v1": {"instance_of": "c4d.Vector", "x": 1, "y": 0, "z": 0},
            "v2": {"instance_of": "c4d.Vector", "x": 0, "y": 1, "z": 0},
            "v3": {"instance_of": "c4d.Vector", "x": 0, "y": 0, "z": 1},
        }

        self.assertDictEqual(result, result_expected)

    def test_serialize_base_container_as_dict(self):
        bc = c4d.BaseContainer()
        bc[1001] = c4d.Vector()
        bc[1002] = c4d.Vector()

        result = serialize.serialize_basecontainer_as_dict(bc)
        result_expected = {
            "instance_of": "c4d.BaseContainer",
            1001: {"instance_of": "c4d.Vector", "x": 0, "y": 0, "z": 0},
            1002: {"instance_of": "c4d.Vector", "x": 0, "y": 0, "z": 0},
        }

        self.assertDictEqual(result, result_expected)

    def test_serialize_baselist2d_as_dict(self):
        base_object = c4d.BaseList2D(c4d.Onull)
        base_object.SetName("Foobar")

        result = serialize.serialize_baselist2d_as_dict(base_object)
        result_expected = {
            "instance_of": "c4d.BaseList2D",
            "name": "Foobar",
            "type": c4d.Onull,
            "data": {},
        }

        try:
            dictutils.assert_is_subset(result_expected, result)
        except exceptions.ComparisonBaseError as e:
            raise AssertionError(e) from e

    def test_serialize_baseobject_as_dict(self):
        base_object = utilities.create_example_baseobject()

        result = serialize.serialize_baseobject_as_dict(base_object, True)
        result_expected = {
            "instance_of": "c4d.BaseObject",
            "name": "Asset_Grp",
            "type": c4d.Onull,
            "data": {},
            "children": [
                {
                    "instance_of": "c4d.BaseObject",
                    "name": "Rig_Grp",
                    "type": c4d.Onull,
                    "data": {},
                    "children": [
                        {
                            "instance_of": "c4d.BaseObject",
                            "name": "Joints_Grp",
                            "type": c4d.Onull,
                            "data": {},
                            "children": [],
                        },
                        {
                            "instance_of": "c4d.BaseObject",
                            "name": "Ctrls_Grp",
                            "type": c4d.Onull,
                            "data": {},
                            "children": [],
                        },
                    ],
                },
                {
                    "instance_of": "c4d.BaseObject",
                    "name": "Geo_Grp",
                    "type": c4d.Onull,
                    "data": {},
                    "children": [],
                },
            ],
        }

        try:
            dictutils.assert_is_subset(result_expected, result)
        except exceptions.ComparisonBaseError as e:
            raise AssertionError(e) from e

    def test_serialize_basetag_as_dict(self):
        base_tag = utilities.create_example_basetag()

        result = serialize.serialize_basetag_as_dict(base_tag)
        result_expected = {
            "instance_of": "c4d.BaseTag",
            "name": "Constraint",
            "type": 1019364,
            "data": {},
        }

        try:
            dictutils.assert_is_subset(result_expected, result)
        except exceptions.ComparisonBaseError as e:
            raise AssertionError(e) from e

    def test_serialize_dagbaseobject_as_dict(self):
        base_object = utilities.create_example_dagbaseobject()

        result = serialize.serialize_dagbaseobject_as_dict(base_object, True)
        result_expected = {
            "instance_of": "c4d.BaseObject",
            "name": "Asset_Grp",
            "type": c4d.Onull,
            "data": {},
            "children": [
                {
                    "instance_of": "c4d.BaseObject",
                    "name": "Rig_Grp",
                    "type": c4d.Onull,
                    "data": {},
                    "children": [
                        {
                            "instance_of": "c4d.BaseObject",
                            "name": "Joints_Grp",
                            "type": c4d.Onull,
                            "data": {},
                            "children": [],
                        },
                        {
                            "instance_of": "c4d.BaseObject",
                            "name": "Ctrls_Grp",
                            "type": c4d.Onull,
                            "data": {},
                            "children": [],
                        },
                    ],
                },
                {
                    "instance_of": "c4d.BaseObject",
                    "name": "Geo_Grp",
                    "type": c4d.Onull,
                    "data": {},
                    "children": [],
                },
            ],
        }

        try:
            dictutils.assert_is_subset(result_expected, result)
        except exceptions.ComparisonBaseError as e:
            raise AssertionError(e) from e

    def test_serialize_dagbasetag_as_dict(self):
        base_tag = utilities.create_example_dagbasetag()

        result = serialize.serialize_dagbasetag_as_dict(base_tag)
        result_expected = {
            "instance_of": "c4d.BaseTag",
            "name": "Constraint",
            "type": 1019364,
            "data": {},
        }

        try:
            dictutils.assert_is_subset(result_expected, result)
        except exceptions.ComparisonBaseError as e:
            raise AssertionError(e) from e

    def test_serialize_layerobjec_as_dict(self):
        layer_object = c4d.documents.LayerObject()

        result = serialize.serialize_layerobject_as_dict(layer_object)
        result_expected = {
            "instance_of": "c4d.documents.LayerObject",
            "name": "Layer",
        }

        try:
            dictutils.assert_is_subset(result_expected, result)
        except exceptions.ComparisonBaseError as e:
            raise AssertionError(e) from e


if __name__ == "__main__":
    unittest.main()
