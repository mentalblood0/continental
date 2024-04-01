import dataclasses
import pathlib
import typing

from .Dict import Dict
from .Net import Net


@dataclasses.dataclass
class Markov:
    dictionary: Dict
    net: Net
    current: int = 0

    def next(self):
        self.current = self.net.next(self.current)
        return self.dictionary[self.current]

    def create(self, paths: typing.Set[pathlib.Path], encoding: str = "utf8"):
        words: typing.Dict[str, int] = {}
        net: typing.Dict[int, typing.Dict[int, int]] = {}

        for p in paths:
            w = ""
            last: typing.Union[int, None] = None

            with p.open("r", encoding=encoding) as f:
                while c := f.read(1):
                    if c.isalpha():
                        w += c.lower()
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
                        last = i
                        w = ""

        self.dictionary.create(
            [t[0] for t in list(sorted(words.items(), key=lambda w: w[1]))]
        )
        self.net.create([tuple([a[0], [b for b in a[1].items()]]) for a in net.items()])
