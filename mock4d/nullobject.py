from mock4d.baseobject import BaseObject
from mock4d.symbols import Onull


class NullObject(BaseObject):
    """
    This class represents a Null Object
    """

    def __init__(self):
        super(NullObject, self).__init__(Onull)
