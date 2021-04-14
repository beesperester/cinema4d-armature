import c4d
import unittest

from typing import List

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

        result = serialize.serialize_base_container_as_dict(bc)
        result_expected = {
            "instance_of": "c4d.BaseContainer",
            1001: {"instance_of": "c4d.Vector", "x": 0, "y": 0, "z": 0},
            1002: {"instance_of": "c4d.Vector", "x": 0, "y": 0, "z": 0},
        }

        self.assertDictEqual(result, result_expected)


if __name__ == "__main__":
    unittest.main()
