from typing import Optional
import c4d

from typing import Optional, Iterator


def IterateHierarchy(op: Optional[c4d.GeListNode]) -> Iterator[c4d.GeListNode]:
    while op:
        yield op

        yield from IterateHierarchy(op.GetDown())

        op = op.GetNext()
