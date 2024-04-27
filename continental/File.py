import dataclasses
import io
import pathlib
import typing


@dataclasses.dataclass
class File:
    path: pathlib.Path

    def __post_init__(self):
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

    @classmethod
    def write(
        cls,
        f: io.BytesIO,
        content: typing.Union[typing.List[typing.Tuple[int, int]], int, bytes],
        length: typing.Union[int, None] = None,
    ):
        if isinstance(content, int):
            if length is None:
                raise ValueError
            content = [(content, length)]
        if isinstance(content, bytes):
            f.write(content)
        elif isinstance(content, list):
            f.write(b"".join(cls.encode(integer, length) for integer, length in content))
        else:
            raise NotImplementedError
