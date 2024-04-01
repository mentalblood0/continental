import dataclasses
import functools
import pathlib
import typing


@dataclasses.dataclass
class Dict:
    path: pathlib.Path

    @functools.cached_property
    def source(self):
        return self.path.open("rb")

    @functools.cached_property
    def max_word_length(self):
        s = self.source
        s.seek(0)
        return int(s.readline())

    @functools.cached_property
    def start(self):
        return len(str(self.max_word_length)) + 1

    def __getitem__(self, key: int):
        s = self.source
        s.seek(self.start + self.max_word_length * key)
        return s.read(self.max_word_length).rstrip().decode()

    def create(self, words: typing.List[str]):
        max_word_length = len(max(words, key=lambda w: len(w)))
        with self.path.open("w") as f:
            f.write(f"{max_word_length}\n")
            for w in words:
                f.write(f"{w:{max_word_length}}")
