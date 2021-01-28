from typing import Optional


class Vector:

    def __init__(
        self,
        x: float,
        y: Optional[float] = None,
        z: Optional[float] = None
    ) -> None:
        if y is None:
            y = x

        if z is None:
            z = x

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)


class Matrix:

    def __init__(
        self,
        v1: Vector,
        v2: Vector,
        v3: Vector,
        off: Vector
    ) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.off = off
