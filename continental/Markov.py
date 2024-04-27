import dataclasses
import io
import random
import typing

from .Dict import Dict
from .Net import Net


@dataclasses.dataclass
class Markov:
    dictionary: Dict
    net: Net
    encoding: str
    current: typing.Union[int, None] = None
    letters: str = "qwertyuiopasdfghjklzxcvbnmйцукенгшщзхфывапролджэячсмитьбюъё"

    def shuffle(self):
        self.current = random.randrange(0, len(self.dictionary))

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            self.shuffle()
        assert self.current is not None

        while True:
            result = self.net.next(self.current)
            if result == self.current:
                self.shuffle()
            else:
                self.current = result
                break

        return self.dictionary[self.current]

    def create(self, stream: io.BytesIO, limit: typing.Union[int, None] = None):
        words: typing.Dict[str, int] = {}
        net: typing.Dict[int, typing.Dict[int, int]] = {}

        w = ""
        last: typing.Union[int, None] = None

        for line in stream:
            for c in line.decode(encoding=self.encoding):
                if c == "\n":
                    continue
                if c in self.letters:
                    w += c
                    continue

                if w:
                    if w not in words:
                        words[w] = len(words)
                    i = words[w]
                    if last is not None:
                        if last not in net:
                            net[last] = {}
                        if i not in net[last]:
                            net[last][i] = 0
                        net[last][i] += 1
                    if limit is not None:
                        limit -= 1
                        if limit == 0:
                            break
                    last = i
                    w = ""

        stream.close()

        self.dictionary.create([t[0] for t in list(sorted(words.items(), key=lambda w: w[1]))])
        self.net.create(
            [tuple[int, list[tuple[int, int]]]([a[0], [b for b in set(a[1].items())]]) for a in net.items() if a[1]]
        )
