import dataclasses
import functools
import typing

from .File import File


@dataclasses.dataclass
class Dict(File):
    words_number_size: int = 4
    word_length_size: int = 1
    word_position_size: int = 4

    @functools.cached_property
    def ids_positions_start(self):
        self.source.seek(0)
        return self.decode(self.source.read(self.word_position_size))

    @functools.cached_property
    def size(self):
        self.source.seek(self.word_position_size)
        return self.decode(self.source.read(self.words_number_size))

    def __len__(self):
        return self.size

    def __getitem__(self, key: int):
        assert key < len(self)
        self.source.seek(self.ids_positions_start + (self.word_position_size + self.word_length_size) * key)
        position = self.read_integer(self.word_position_size)
        size = self.read_integer(self.word_length_size)
        assert size
        self.source.seek(position)
        return self.read_bytes(size).decode()

    @property
    def structure(self):
        result = {}
        f = self.source
        self.source.seek(0)

        result["ids_positions_start"] = self.read_integer(self.word_position_size)
        result["size"] = self.read_integer(self.words_number_size)
        words_position = f.tell()

        f.seek(result["ids_positions_start"])
        result["positions_and_lengths"] = []
        for _ in range(result["size"]):
            position = self.read_integer(self.word_position_size)
            length = self.read_integer(self.word_length_size)
            result["positions_and_lengths"].append([position, length])

        f.seek(words_position)
        result["words"] = []
        for _, length in result["positions_and_lengths"]:
            result["words"].append(f.read(length))

        return result

    def check(self):
        for i in range(len(self)):
            self[i]

    def create(self, words: typing.List[str]):
        with self.path.open("wb") as f:
            f.seek(self.word_position_size + self.words_number_size)

            positions_and_lengths: typing.List[typing.Tuple[int, int]] = []
            for w in words:
                w_bytes = w.encode()
                positions_and_lengths.append((f.tell(), len(w_bytes)))
                f.write(w_bytes)

            ids_positions_start = f.tell()

            for p, l in positions_and_lengths:
                f.write(self.encode(p, self.word_position_size) + self.encode(l, self.word_length_size))

            f.seek(0)
            f.write(self.encode(ids_positions_start, self.word_position_size))
            f.write(self.encode(len(words), self.words_number_size))
