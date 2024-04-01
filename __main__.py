import pathlib

from .Dict import Dict
from .Markov import Markov
from .Net import Net

m = Markov(Dict(pathlib.Path("mn/kapital.mnd")), Net(pathlib.Path("mn/kapital.mnn")))
m.create({pathlib.Path("mn/kapital.txt")}, "cp1251")

for _ in range(10):
    print(m.next())
