import c4d

from rigging.modules.shape import ObjectShape
from rigging.modules.shape.validators import (
    NameValidator,
    InstanceValidator
)

asset_shape = ObjectShape(
    "asset",
    [
        NameValidator("Asset_Grp"),
        InstanceValidator(c4d.Onull)
    ]
)