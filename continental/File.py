import dataclasses
import pathlib


@dataclasses.dataclass
class File:
    path: pathlib.Path

    def __post_init__(self):
        self.path.touch(exist_ok=True)
        self.source = self.path.open("rb")

    @classmethod
    def encode(cls, i: int, length: int):
        return i.to_bytes(length, byteorder="big")

    @classmethod
    def decode(cls, b: bytes):
        return int.from_bytes(b, byteorder="big")

    def _read(self, length: int):
        b = self.source.read(length)
        if not b:
            raise EOFError
        return b

    def read_integer(self, length: int):
        return self.decode(self._read(length))

    def read_bytes(self, length: int):
        return self._read(length)
