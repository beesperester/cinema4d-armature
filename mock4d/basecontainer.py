from typing import Any, Dict


class BaseContainer:
    """
    This class represents a Base Container
    """

    def __init__(self):
        self._data: Dict[str, Any] = {}

    def __setitem__(self, key: str, value: Any):
        if not hasattr(self, key):
            self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        if not hasattr(self, key):
            return self._data[key]
