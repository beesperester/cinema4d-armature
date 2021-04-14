import typing
import logging

from armature import dag


class ArmatureModule:
    def __init__(
        self,
        dag_object: dag.DagBaseObject,
        adapters: dag.DagBaseObjectList,
        modules: typing.Optional[typing.List["ArmatureModule"]] = None,
    ) -> None:
        if modules is None:
            modules = []

        self._dag_object = dag_object
        self._adapters = adapters
        self._modules = modules
        self._objects = dag.DagBaseObjectList()
        self._tags = dag.DagBaseTagList()

    def ExtendObjects(self, adapters: dag.DagBaseObjectList) -> None:
        self.GetAdapters().Extend(adapters)
        self.GetObjects().Extend(adapters)

    def AppendAdapter(self, adapter: dag.DagBaseObject) -> None:
        self.GetAdapters().Append(adapter)
        self.GetObjects().Append(adapter)

    def ExtendTags(self, tags: dag.DagBaseTagList) -> None:
        self.GetTags().Extend(tags)

    def AppendTag(self, tag: dag.DagBaseTag) -> None:
        self.GetTags().Append(tag)

    def GetDagObject(self) -> dag.DagBaseObject:
        return self._dag_object

    def GetAdapters(self) -> dag.DagBaseObjectList:
        return self._adapters

    def GetObjects(self) -> dag.DagBaseObjectList:
        return self._objects

    def GetTags(self) -> dag.DagBaseTagList:
        return self._tags

    def GetModules(self) -> typing.List["ArmatureModule"]:
        return self._modules

    def _PreSetup(self) -> None:
        logging.info(f"{self.__class__.__name__}::PreSetup")

        self.PreSetup()

    def _Setup(self) -> None:
        logging.info(f"{self.__class__.__name__}::Setup")

        self.Setup()

    def _PostSetup(self) -> None:
        logging.info(f"{self.__class__.__name__}::PostSetup")

        self.PostSetup()

    def _TearDown(self) -> None:
        logging.info(f"{self.__class__.__name__}::TearDown")

        self.TearDown()

    def PreSetup(self) -> None:
        # will be called before the actual setup
        # place anything that needs to be prepared
        # or done before in here like validation
        pass

    def Setup(self) -> None:
        raise NotImplementedError()

    def PostSetup(self) -> None:
        # will be called after the actual setup
        # place anything that needs to be prepared
        # or done after in here like validation
        pass

    def TearDown(self) -> None:
        # this will be called in the case of an exception
        # thrown during the mount process and should be used
        # to clean up any effects
        pass

    def Mount(self) -> None:
        logging.info(f"{self.__class__.__name__}::Mount")

        try:
            # setup self
            self._PreSetup()

            self._Setup()

            self._PostSetup()

            # setup depending modules
            for module in self.GetModules():
                module.Mount()
        except Exception as e:
            # teardown self
            self._TearDown()

            # re-raise exception to teardown nested effects
            raise e


class Armature:
    def __init__(self, root_module: ArmatureModule):
        self._root_module = root_module

    def GetRoot(self) -> ArmatureModule:
        return self._root_module

    def Mount(self):
        self.GetRoot().Mount()
