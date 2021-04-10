import typing
import logging

from armature import dag


class ArmatureModule:
    def __init__(
        self,
        dag_object: dag.DagObject,
        adapters: dag.DagObjects,
        modules: typing.Optional[typing.List["ArmatureModule"]] = None,
    ) -> None:
        if modules is None:
            modules = []

        self._dag_object = dag_object
        self._adapters = adapters
        self._modules = modules

    def GetDagObject(self) -> dag.DagObject:
        return self._dag_object

    def GetAdapters(self) -> dag.DagObjects:
        return self._adapters

    def GetModules(self) -> typing.List["ArmatureModule"]:
        return self._modules

    def _PreSetup(self) -> None:
        logging.info("PreSetup '{}'".format(self.__class__.__name__))

        self.PreSetup()

    def _Setup(self) -> None:
        logging.info("Setup '{}'".format(self.__class__.__name__))

        self.Setup()

    def _PostSetup(self) -> None:
        logging.info("PostSetup '{}'".format(self.__class__.__name__))

        self.PostSetup()

    def PreSetup(self) -> None:
        pass

    def Setup(self) -> None:
        raise NotImplementedError()

    def PostSetup(self) -> None:
        pass

    def Mount(self) -> None:
        logging.info("Mount '{}'".format(self.__class__.__name__))

        # setup self
        self._PreSetup()

        self._Setup()

        self._PostSetup()

        # setup depending modules
        for module in self.GetModules():
            module.Mount()


class Armature:
    def __init__(self, root_module: ArmatureModule):
        self._root_module = root_module

    def GetRoot(self) -> ArmatureModule:
        return self._root_module

    def Mount(self):
        self.GetRoot().Mount()
