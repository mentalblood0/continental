import dataclasses
import functools
import random
import typing

from .File import File


@dataclasses.dataclass
class Net(File):
    word_identifier_size: int = 4
    next_words_number_size: int = 3
    word_frequency_size: int = 1
    word_identifier_position_size: int = 5

    @functools.cached_property
    def frequency_norm(self):
        return 2 ** (8 * self.word_frequency_size) - 1

    def normalized(self, next_words: typing.List[typing.Tuple[int, int]]):
        m = max(n[1] for n in next_words)
        return sorted(((int(n[1] / m * self.frequency_norm) or 1, n[0]) for n in next_words), key=lambda o: -o[0])

    @functools.cached_property
    def ids_positions_start(self):
        f = self.source
        temp = f.tell()
        f.seek(0)
        result = self.read_integer(self.word_identifier_position_size)
        f.seek(temp)
        return result

    def create(self, d: typing.List[typing.Tuple[int, typing.List[typing.Tuple[int, int]]]]):
        ids_positions = [0]
        for p in d:
            ids_positions.append(
                ids_positions[-1]
                + self.word_identifier_size
                + self.next_words_number_size
                + len(p[1]) * (self.word_frequency_size + self.word_identifier_position_size)
            )

        with self.path.open("wb") as f:
            f.seek(self.word_identifier_position_size)
            for p in d:
                f.write(
                    self.encode(p[0], self.word_identifier_size)
                    + self.encode(len(p[1]), self.next_words_number_size)
                    + b"".join(
                        self.encode(n[0], self.word_frequency_size)
                        + self.encode(
                            ids_positions[n[1]] + self.word_identifier_position_size, self.word_identifier_position_size
                        )
                        for n in self.normalized(p[1])
                    )
                )
            ids_positions_start = f.tell()
            for i in ids_positions:
                f.write(self.encode(i + self.word_identifier_position_size, self.word_identifier_position_size))
            f.seek(0)
            f.write(self.encode(ids_positions_start, self.word_identifier_position_size))

    @property
    def structure(self):
        result = {}
        f = self.source
        f.seek(0)
        result["ids_positions_start"] = self.read_integer(self.word_identifier_position_size)
        result["words"] = []

        while f.tell() < result["ids_positions_start"]:
            word = {}
            word["identifier"] = self.read_integer(self.word_identifier_size)
            word["number_of_next"] = self.read_integer(self.next_words_number_size)
            word["next_words"] = []
            for _ in range(word["number_of_next"]):
                next_word = {}
                next_word["frequency"] = self.read_integer(self.word_frequency_size)
                next_word["position"] = self.read_integer(self.word_identifier_position_size)
                word["next_words"].append(next_word)
            result["words"].append(word)

        result["words_positions"] = []
        for _ in range(len(result["words"])):
            result["words_positions"].append(self.read_integer(self.word_identifier_position_size))

        return result

    def next(self, current: int):
        f = self.source
        f.seek(0)

        f.seek(self.ids_positions_start + current * self.word_identifier_position_size)
        p = self.read_integer(self.word_identifier_position_size)

        f.seek(p + self.word_identifier_size)
        next_words_number = self.read_integer(self.next_words_number_size)

        for i in range(next_words_number):
            total_frequency_left = self.frequency_norm * (next_words_number - i)
            current_frequency = self.read_integer(self.word_frequency_size)
            position = self.read_integer(self.word_identifier_position_size)

            if (random.uniform(0, 1) <= (current_frequency / total_frequency_left)) or (i == next_words_number - 1):
                f.seek(position)
                return self.read_integer(self.word_identifier_size)

        raise NotImplementedError
