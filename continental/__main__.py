import argparse
import itertools
import json
import pathlib
import sys

from . import adapters
from .Dict import Dict
from .Markov import Markov
from .Net import Net

parser = argparse.ArgumentParser(
    prog="Continental", description="Create on-disk Markov chain and generate text using it"
)
subparsers = parser.add_subparsers(dest="subparser_name")

create = subparsers.add_parser("create")
create.add_argument("-o", "--output", type=pathlib.Path, required=True)
create.add_argument("-e", "--encoding", type=str, default="utf8")

generate = subparsers.add_parser("generate")
generate.add_argument("-i", "--input", type=pathlib.Path, required=True)
generate.add_argument("-l", "--limit", type=int, required=True)

adapt = subparsers.add_parser("adapt")
adapt.add_argument("-e", "--encoding", type=str, default="utf8")
adapters = {name.lower(): getattr(adapters, name) for name in dir(adapters) if not name.startswith("_")}
adapt.add_argument("-m", "--mode", type=str, required=True, default=next(iter(adapters)), choices=[*adapters.keys()])
adapt.add_argument("-c", "--config", type=str, required=False, default="{}")

args = parser.parse_args()

if args.subparser_name == "create":
    args.output.mkdir(parents=True, exist_ok=True)
    m = Markov(Dict(args.output / "dictionary"), Net(args.output / "net"), args.encoding).create(sys.stdin.buffer)

elif args.subparser_name == "generate":
    if args.limit <= 0:
        exit()

    assert args.input.isdir()
    m = Markov(Dict(args.input / "dictionary"), Net(args.input / "net"))

    for word in itertools.islice(m.text, args.limit):
        sys.stdout.write(word)
    sys.stdout.write(".\n")

elif args.subparser_name == "adapt":
    for chunk in adapters[args.mode](sys.stdin.buffer, **json.loads(args.config))():
        sys.stdout.write(chunk)
