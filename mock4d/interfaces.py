from __future__ import annotations

from typing import Optional, List

from mock4d import gelistnode


class ILayerObject:
    """
    This class represents a Layer Object
    """


class IBaseDocument:
    """
    This class represents a Base Document
    """

    def __init__(
        self,
    ) -> None:
        raise NotImplementedError(
            "{} must implement '__init__'".format(self.__class__.__name__)
        )

    def GetLayerObjectRoot(self) -> gelistnode.GeListNode:
        raise NotImplementedError(
            "{} must implement 'GetLayerObjectRoot'".format(
                self.__class__.__name__
            )
        )


class IBaseObject:
    """
    This class represents a Base Object Interface
    """

    # def __init__(
    #     self,
    #     atom_type: int
    # ) -> None:
    #     raise NotImplementedError(
    #         "{} must implement '__init__'".format(self.__class__.__name__)
    #     )

    def GetTags(self) -> List[IBaseTag]:
        raise NotImplementedError(
            "{} must implement 'GetTags'".format(self.__class__.__name__)
        )

    def InsertTag(
        self,
        tp: IBaseTag,
        pred: Optional[IBaseTag] = None
    ) -> None:
        raise NotImplementedError(
            "{} must implement 'InsertTag'".format(self.__class__.__name__)
        )

    def MakeTag(
        self,
        x: int,
        pred: Optional[IBaseTag] = None
    ) -> IBaseTag:
        raise NotImplementedError(
            "{} must implement 'MakeTag'".format(self.__class__.__name__)
        )


class IBaseTag:
    """
    This class represents a Base Tag Interface
    """

    # def __init__(
    #     self,
    #     atom_type: int
    # ) -> None:
    #     raise NotImplementedError(
    #         "{} must implement '__init__'".format(self.__class__.__name__)
    #     )

    def GetObject(self) -> Optional[IBaseObject]:
        raise NotImplementedError(
            "{} must implement 'GetObject'".format(self.__class__.__name__)
        )

    def SetObject(
        self,
        op: IBaseObject
    ) -> None:
        raise NotImplementedError(
            "{} must implement 'SetObject'".format(self.__class__.__name__)
        )

    def GetName(
        self
    ) -> str:
        raise NotImplementedError(
            "{} must implement 'GetName'".format(self.__class__.__name__)
        )

    def SetName(
        self,
        name: str
    ) -> None:
        raise NotImplementedError(
            "{} must implement 'SetName'".format(self.__class__.__name__)
        )
