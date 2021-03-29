from __future__ import annotations

import typing

import fnmatch

from armature import interfaces, dag


class NameValidationRule(interfaces.IValidationRule):
    def __init__(self, name_pattern: str) -> None:
        self._name_pattern = name_pattern

    def Test(
        self, validator: interfaces.IValidator, base_object: dag.DagObject
    ) -> bool:
        """
        Validate the given name string against the name pattern
        using fnmatch
        """

        name: str = base_object.GetObject().GetName()  # type: ignore

        if not fnmatch.fnmatch(name, self._name_pattern):
            raise Exception(
                "{}: Object must match pattern '{}' is '{}'".format(
                    validator.GetName(), self._name_pattern, name
                )
            )

        return True


class InstanceValidationRule(interfaces.IValidationRule):
    def __init__(self, type_id: int) -> None:
        self._type_id = type_id

    def Test(
        self, validator: interfaces.IValidator, base_object: dag.DagObject
    ) -> bool:
        """
        Validate the given name string against the name pattern
        using fnmatch
        """

        if not base_object.GetObject().IsInstanceOf(self._type_id):
            raise Exception(
                "{}: Object must be an instance of '{}' is '{}'".format(
                    validator.GetName(),
                    self._type_id,
                    base_object.GetObject().GetType(),
                )
            )

        return True


class BaseValidator(interfaces.IValidator):
    def __init__(
        self,
        name: str,
        rules: typing.Optional[typing.List[interfaces.IValidationRule]] = None,
    ):
        if rules is None:
            rules = []

        self._name = name
        self._rules = rules

    def GetName(self) -> str:
        return self._name

    def GetRules(
        self,
    ) -> typing.List[interfaces.IValidationRule]:
        return self._rules


class RecursiveObjectValidator(BaseValidator):
    def __init__(
        self,
        object_validator: "ObjectValidator",
        end_object_validator: typing.Optional["ObjectValidator"] = None,
    ) -> None:
        self._object_validator = object_validator
        self._end_object_validator = end_object_validator

    def HasEndObjectValidator(self) -> bool:
        return bool(self._end_object_validator)

    def Validate(self, base_object: dag.DagObject) -> None:
        self._object_validator.Validate(base_object)

        exception = None

        for child_base_object in base_object.GetChildren():
            try:
                self.Validate(child_base_object)

                exception = None

                break
            except Exception as e:
                # if no child base object matches the object validator
                # try and match the child to the end object validator
                if self.HasEndObjectValidator():
                    try:
                        self._end_object_validator.Validate(child_base_object)

                        exception = None

                        break
                    except Exception as e:
                        exception = e
                else:
                    exception = e

        if exception:
            raise exception


class ObjectValidator(BaseValidator):
    def __init__(
        self,
        name: str,
        rules: typing.Optional[typing.List[interfaces.IValidationRule]] = None,
        children: typing.Optional[typing.List[ObjectValidator]] = None,
    ):
        if children is None:
            children = []

        self._children = children

        super().__init__(name, rules)

    def Validate(self, base_object: dag.DagObject) -> None:
        # test own rules
        for validation_rule in self.GetRules():
            validation_rule.Test(self, base_object)

        # test children
        results = []
        exceptions = []

        child_object_validators = self.GetChildren()

        for child_object_shape in child_object_validators:
            for child_base_object in base_object.GetChildren():
                try:
                    child_object_shape.Validate(child_base_object)

                    results.append(True)
                except Exception as e:
                    exceptions.append(e)

        if len(results) < len(child_object_validators):
            if len(exceptions) > 0:
                exceptions.reverse()

                raise exceptions.pop()
            else:
                raise Exception("No child object matches shape")

    def Get(self, path: str) -> ObjectValidator:
        child_names: typing.List[str] = [
            x.GetName() for x in self.GetChildren()
        ]

        parts = path.split("/")

        if len(parts) > 0:
            name = parts[0]
            child_index = -1

            # use fnmatch against the list of child names
            # if name contains an asterisk
            if "*" in name:
                matching_child_names = fnmatch.filter(child_names, name)

                if matching_child_names:
                    child_index = child_names.index(matching_child_names[0])
            # use name as is against list of child names
            else:
                if name in child_names:
                    child_index = child_names.index(name)

            # use child index to retrieve base object
            # if child index is larger -1
            if child_index > -1:
                child = self.GetChildren()[child_index]

                if len(parts) > 1:
                    return child.Get("/".join(parts[1:]))
                else:
                    return child

        raise Exception(
            "'{}' has no child object called '{}'".format(
                self.__class__.__name__, path
            )
        )

    def GetChildren(self) -> typing.List[ObjectValidator]:
        return self._children
