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
        self._object_effects = dag.DagBaseObjectList()
        self._tag_effects = dag.DagBaseTagList()

    def CaptureEffects(
        self, generator: typing.Generator[dag.DagAtom, None, None]
    ) -> None:
        for effect in generator:
            if isinstance(effect, dag.DagBaseTag):
                self.GetTagEffects().Append(effect)
            elif isinstance(effect, dag.DagBaseObject):
                self.GetObjecEffects().Append(effect)
                self.GetAdapters().Append(effect)

    def GetDagObject(self) -> dag.DagBaseObject:
        return self._dag_object

    def GetAdapters(self) -> dag.DagBaseObjectList:
        return self._adapters

    def GetObjecEffects(self) -> dag.DagBaseObjectList:
        return self._object_effects

    def GetTagEffects(self) -> dag.DagBaseTagList:
        return self._tag_effects

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

        # remove object effects
        for object_effect in self.GetObjecEffects():
            object_effect.Remove()

        # remove tag effects
        for tag_effect in self.GetTagEffects():
            tag_effect.Remove()

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
