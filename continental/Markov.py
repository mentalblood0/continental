import dataclasses
import sys
import codecs
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
    punctuation: str = ',:-.!?;'

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

    def create(self, stream: typing.Union[io.BytesIO, sys.stdin.buffer.__class__]):
        words: typing.Dict[str, int] = {}
        net: typing.Dict[int, typing.Dict[int, int]] = {}

        w = ""
        last: typing.Union[int, None] = None
        encoded = codecs.iterdecode(stream, self.encoding)

        def add(word: str):
            nonlocal last
            nonlocal words
            nonlocal net
            if word not in words:
                words[word] = len(words)
            i = words[word]
            if last is not None:
                if last not in net:
                    net[last] = {}
                if i not in net[last]:
                    net[last][i] = 0
                net[last][i] += 1
            last = i

        for line in encoded:
            for c in line:
                if c in self.punctuation:
                    if w:
                        add(w)
                        w = ""
                    add(c)
                    continue
                else:
                    if (c := c.lower()) in self.letters:
                        w += c
                        continue
                if w:
                    add(w)
                    w = ""


        encoded.close()

        self.dictionary.create([t[0] for t in list(sorted(words.items(), key=lambda w: w[1]))])
        self.net.create(
            [tuple[int, list[tuple[int, int]]]([a[0], [b for b in set(a[1].items())]]) for a in net.items() if a[1]]
        )
