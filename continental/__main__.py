import argparse
import itertools
import pathlib
import sys

from .Dict import Dict
from .Markov import Markov
from .Net import Net

parser = argparse.ArgumentParser(
    prog="Continental", description="Create on-disk markov chain and generate text using it"
)
parser.add_argument("-m", "--mode", default="generate", choices=["create", "generate"])
parser.add_argument("-d", "--dictionary", type=pathlib.Path, required=True)
parser.add_argument("-n", "--net", type=pathlib.Path, required=True)
parser.add_argument("-l", "--limit", type=int, default=None)
parser.add_argument("-e", "--encoding", type=str, default="utf8")
args = parser.parse_args()

m = Markov(Dict(args.dictionary), Net(args.net), args.encoding)
if args.mode == "create":
    m.create(sys.stdin.buffer)
elif args.mode == "generate":
    if not args.limit:
        exit()

    for word in itertools.islice(m.text, args.limit):
        sys.stdout.write(word)
    sys.stdout.write(".\n")
