class BaseError(Exception):
    def __init__(self, text: str) -> None:
        self.text = text
        super().__init__(text)


class CallableError(BaseError):
    def __str__(self) -> str:
        return f"{self.text} is not Callable."


class NotEnoughError(BaseError):
    def __str__(self) -> str:
        return f"Not enough {self.text} are provided."
