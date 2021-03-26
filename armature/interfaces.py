from typing import Protocol


class INamed(Protocol):
    def GetName(self) -> str:
        return ""
