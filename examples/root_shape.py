import c4d

from rigging.modules.shape import ObjectShape
from rigging.modules.shape.validators import (
    NameValidator,
    InstanceValidator
)

root_shape = ObjectShape(
    "root",
    [
        NameValidator("Root_Joint"),
        InstanceValidator(c4d.Ojoint)
    ]
)