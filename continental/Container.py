import dataclasses
import typing

from .File import File


@dataclasses.dataclass
class Container(File):
    inner: typing.List[File] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        for f in self.inner:
            f.start += self.start
