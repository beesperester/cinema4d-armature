import c4d


class IValidator:

    def Validate(
        self,
        op: c4d.BaseObject
    ) -> bool:
        raise NotImplementedError(
            "Bound method 'Validate' must be implemented"
        )
