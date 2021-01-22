class Messagebag(list):
    """
    This class implements a message bag for holding messages
    """


class Message:

    def __init__(
        self,
        message: str
    ) -> None:
        self._message = message
    
    def GetMessage(self) -> str:
        return self._message
