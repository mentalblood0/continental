import dataclasses
import codecs
import typing
import sys
import abc


@dataclasses.dataclass
class Adapter(abc.ABC):
    source: sys.stdin.buffer.__class__
    encoding: str = "utf8"

    @property
    def text(self):
        return codecs.iterdecode(self.source, self.encoding)

    @abc.abstractmethod
    def __call__(self) -> typing.Generator[str, None, None]: ...
