from typing import Optional, Union


class GoldenSourceError(Exception):
    """GoldenSource Error."""

    def __init__(self, original: Optional[Union[str, Exception]] = None):
        self.original = original
        super().__init__(str(original))
