import dataclasses
import functools
import pathlib
import random
import typing


@dataclasses.dataclass
class Net:
    path: pathlib.Path
    word_identifier_size: int = 4
    next_words_number_size: int = 3
    word_frequency_size: int = 1
    word_identifier_position_size: int = 5

    def encode(self, i: int, length: int):
        return i.to_bytes(length, byteorder="big")

    def decode(self, b: bytes):
        return int.from_bytes(b, byteorder="big")

    @functools.cached_property
    def source(self):
        return self.path.open("rb")

    @functools.cached_property
    def frequency_norm(self):
        return 2 ** (8 * self.word_frequency_size) - 1

    def normalized(self, next_words: typing.List[typing.Tuple[int, int]]):
        t = sum(n[0] for n in next_words)
        for n in next_words:
            r = (n[0] * self.frequency_norm // t) or 1
            yield r, n[1]

    @functools.cached_property
    def ids_positions_start(self):
        f = self.source
        temp = f.tell()
        f.seek(0)
        result = self.decode(f.read(self.word_identifier_size))
        f.seek(temp)
        return result

    def create(
        self,
        d: typing.List[typing.Tuple[int, typing.List[typing.Tuple[int, int]]]],
    ):
        ids_positions = [0]
        for p in d:
            ids_positions.append(
                ids_positions[-1]
                + self.word_identifier_size
                + self.next_words_number_size
                + len(p[1])
                * (self.word_frequency_size + self.word_identifier_position_size)
            )

        with self.path.open("wb") as f:
            f.write(
                self.encode(
                    ids_positions[-1] + self.word_identifier_size,
                    self.word_identifier_size,
                )
            )
            for p in d:
                f.write(
                    self.encode(p[0], self.word_identifier_size)
                    + self.encode(len(p[1]), self.next_words_number_size)
                    + b"".join(
                        self.encode(n[0], self.word_frequency_size)
                        + self.encode(n[1], self.word_identifier_position_size)
                        for n in self.normalized(p[1])
                    )
                )
            ids_positions_start = f.tell()
            for i in ids_positions:
                f.write(self.encode(i + ids_positions_start, self.word_identifier_size))

    def next(self, current: int):
        f = self.source

        f.seek(self.ids_positions_start + current * self.word_identifier_position_size)
        p = self.decode(f.read(self.word_identifier_position_size))

        f.seek(p)
        next_words_number = self.decode(f.read(self.next_words_number_size))
        for i in range(next_words_number - 1):
            total_frequency_left = self.frequency_norm * (next_words_number - i)
            current_frequency = self.decode(f.read(self.word_frequency_size))
            if random.uniform(0, 1) <= (current_frequency / total_frequency_left):
                position = self.decode(f.read(self.word_identifier_position_size))
                f.seek(position)
                return self.decode(f.read(self.word_identifier_size))
            else:
                f.seek(f.tell() + self.word_identifier_position_size)

        f.seek(f.tell() + self.word_frequency_size)
        position = self.decode(f.read(self.word_identifier_position_size))
        f.seek(position)
        return self.decode(f.read(self.word_identifier_size))
