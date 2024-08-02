import codecs
import dataclasses
import io
import operator
import random
import sys
import typing

from .Dict import Dict
from .Net import Net


@dataclasses.dataclass
class Markov:
    dictionary: Dict
    net: Net
    encoding: str = "utf8"
    current: typing.Union[typing.Tuple[int, str], None] = None
    letters: str = "qwertyuiopasdfghjklzxcvbnmйцукенгшщзхфывапролджэячсмитьбюъё-"
    punctuation: str = ",:"
    endings: str = ".!?;"

    def shuffle(self):
        self.set(random.randrange(0, len(self.dictionary)))

    def set(self, target: int):
        self.current = (target, self.dictionary[target])

    def __iter__(self):
        self.shuffle()
        return self

    def __next__(self):
        if self.current is None:
            self.shuffle()

        while True:
            try:
                assert self.current is not None
                if (result := self.net.next(self.current[0])) == self.current[0]:
                    self.current = None
                    return "."
                self.set(result)
                break
            except EOFError:
                continue

        return self.current[1]

    @property
    def text(self):
        last = None
        for word in self:
            if last is None:
                if word in self.punctuation or word in self.endings:
                    continue
                result = word.capitalize()
            elif last in self.endings:
                if word in self.punctuation or word in self.endings:
                    continue
                result = f" {word.capitalize()}"
            elif word in self.punctuation or word in self.endings:
                result = word
                if word in self.endings:
                    self.current = None
            else:
                result = f" {word}"
            last = word
            yield result

    def create(self, stream: typing.Union[io.BytesIO, sys.stdin.buffer.__class__]):
        words: typing.Dict[str, int] = {}
        net: typing.Dict[int, typing.Dict[int, int]] = {}

        w = ""
        last: typing.Union[int, None] = None

        def add(word: str):
            nonlocal last, words, net

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

        for line in codecs.iterdecode(stream, self.encoding):
            for c in line:
                if (c in self.punctuation) or (c in self.endings):
                    if w:
                        add(w)
                        w = ""
                    add(c)
                elif (c := c.lower()) in self.letters:
                    w += c
                elif w:
                    add(w)
                    w = ""
            if w:
                add(w)
                w = ""

        stream.close()

        self.dictionary.create([t[0] for t in list(sorted(words.items(), key=operator.itemgetter(1)))])
        self.net.create([tuple[int, list[tuple[int, int]]]([a[0], [*a[1].items()]]) for a in net.items() if a[1]])
