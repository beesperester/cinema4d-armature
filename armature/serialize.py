from typing import Any, Dict
import c4d

from armature import dag


def serialize_vector_as_dict(vector: c4d.Vector) -> Dict[str, float]:
    return {
        "instance_of": "c4d.Vector",
        "x": vector.x,  # type: ignore
        "y": vector.y,  # type: ignore
        "z": vector.z,  # type: ignore
    }


def serialize_matrix_as_dict(matrix: c4d.Matrix) -> Dict[str, Dict]:
    return {
        "instance_of": "c4d.Matrix",
        "off": serialize_vector_as_dict(matrix.off),  # type: ignore
        "v1": serialize_vector_as_dict(matrix.v1),  # type: ignore
        "v2": serialize_vector_as_dict(matrix.v2),  # type: ignore
        "v3": serialize_vector_as_dict(matrix.v3),  # type: ignore
    }


def serialize_base_container_as_dict(bc: c4d.BaseContainer) -> Dict[str, Dict]:
    def serialize_value(value: Any) -> Any:
        if isinstance(value, c4d.BaseContainer):
            return serialize_base_container_as_dict(value)
        elif isinstance(value, c4d.Matrix):
            return serialize_matrix_as_dict(value)
        elif isinstance(value, c4d.Vector):
            return serialize_vector_as_dict(value)
        elif isinstance(value, c4d.PriorityData):
            return None
        else:
            return value

    return {
        **{"instance_of": "c4d.BaseContainer"},
        **{key: serialize_value(value) for key, value in bc},  # type: ignore
    }


def serialize_dagbaseobject_as_dict(
    dag_base_object: dag.DagBaseObject,
) -> Dict[str, Any]:
    base_container: c4d.BaseContainer = dag_base_object.item.GetDataInstance()  # type: ignore

    return serialize_base_container_as_dict(base_container)


def serialize_dagbasetag_as_dict(
    dag_base_tag: dag.DagBaseTag,
) -> Dict[str, Any]:
    base_container: c4d.BaseContainer = dag_base_tag.item.GetDataInstance()  # type: ignore

    return serialize_base_container_as_dict(base_container)
