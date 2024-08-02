<h1 align="center">📖 continental</h1>

<h3 align="center">Create on-disk Markov chain and generate text using it</h3>

<p align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://www.python.org/"><img alt="Python version: >=3.11" src="https://img.shields.io/badge/Python-3.11%20|%203.12-blue"></a>
</p>

## Installation

```bash
python -m pip install --upgrade git+https://codeberg.org/mentalblood/continental
```

## Usage

### Create

```bash
cat ~/Downloads/telegram_dumps/*.json | python -m continental adapt -m telegram -c '{"users": ["Степан Нечепоренко"]}' | python -m continental create -o ~/continental_nets/Степан\ Нечепоренко
```

### Generate

```bash
python -m continental generate -i ~/continental_nets/Степан\ Нечепоренко -l 1000
```
