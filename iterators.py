import c4d


def IterateHierarchy(op: c4d.BaseObject):
    while op:
        yield op

        yield from IterateHierarchy(op.GetDown())

        op = op.GetNext()


def IterateChildren(op: c4d.BaseObject):
    while op:
        yield op

        op = op.GetNext()
