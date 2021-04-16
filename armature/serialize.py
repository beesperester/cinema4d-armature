from typing import Any, Dict, Optional
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


def serialize_basecontainer_as_dict(bc: c4d.BaseContainer) -> Dict[str, Dict]:
    def serialize_value(value: Any) -> Any:
        if isinstance(value, c4d.BaseContainer):
            return serialize_basecontainer_as_dict(value)
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


def serialize_baselist2d_as_dict(
    baselist2d: c4d.BaseList2D, recursive: bool = False
):
    doc: c4d.documents.BaseDocument = c4d.documents.GetActiveDocument()  # type: ignore

    layer: Optional[c4d.documents.LayerObject] = baselist2d.GetLayerObject(doc)  # type: ignore

    return {
        "instance_of": "c4d.BaseList2D",
        "name": baselist2d.GetName(),
        "type": baselist2d.GetType(),
        "layer": serialize_layerobject_as_dict(layer) if layer else None,
        "data": serialize_basecontainer_as_dict(
            baselist2d.GetDataInstance()  # type:ignore
        ),
    }


def serialize_layerobject_as_dict(
    layerobject: c4d.documents.LayerObject,
) -> Dict[str, Any]:
    layerobject_data_instance: c4d.BaseContainer = layerobject.GetDataInstance()  # type: ignore

    return {
        "instance_of": "c4d.documents.LayerObject",
        "name": layerobject.GetName(),
        "color": serialize_vector_as_dict(
            layerobject_data_instance[c4d.ID_LAYER_COLOR]  # type: ignore
        ),
    }


def serialize_baseobject_as_dict(
    baseobject: c4d.BaseObject, recursive: bool = False
):
    return {
        **serialize_baselist2d_as_dict(baseobject),
        "instance_of": "c4d.BaseObject",
        "children": [
            serialize_baseobject_as_dict(x, recursive)
            for x in baseobject.GetChildren()  # type: ignore
            if recursive
        ],
    }


def serialize_basetag_as_dict(basetag: c4d.BaseTag):
    return {
        **serialize_baselist2d_as_dict(basetag),
        "instance_of": "c4d.BaseTag",
    }


def serialize_dagbaseobject_as_dict(
    dag_base_object: dag.DagBaseObject, recursive: bool = False
) -> Dict[str, Any]:
    return serialize_baseobject_as_dict(dag_base_object.item, recursive)


def serialize_dagbasetag_as_dict(
    dag_base_tag: dag.DagBaseTag,
) -> Dict[str, Any]:
    return serialize_basetag_as_dict(dag_base_tag.item)
