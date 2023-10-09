class File:
    def __init__(self, name: str, data: bytes):
        """Initialize a file object with the name and binary data."""

        self.name = name
        self.data = data

    @property
    def size(self):
        return len(self.data)
