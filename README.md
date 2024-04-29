<h1 align="center">📖 continental</h1>

<h3 align="center">Create on-disk Markov chain and generate text using it</h3>

<p align="center">
<a href="https://github.com/MentalBlood/continental/blob/master/.github/workflows/lint.yml"><img alt="Lint Status" src="https://github.com/MentalBlood/continental/actions/workflows/lint.yml/badge.svg"></a>
<a href="https://github.com/MentalBlood/continental/blob/master/.github/workflows/complexity.yml"><img alt="Complexity Status" src="https://github.com/MentalBlood/continental/actions/workflows/complexity.yml/badge.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://www.python.org/"><img alt="Python version: >=3.11" src="https://img.shields.io/badge/Python-3.11%20|%203.12-blue"></a>
</p>

## Installation

```bash
python3 -m pip install --upgrade git+https://github.com/mentalblood/continental
```

## Usage

### Create

```bash
cat ~/Downloads/telegram_dumps/* | python -m continental adapt -m telegram -c '{"users": ["Степан Нечепоренко"]}' | python -m continental create -d Степан\ Нечепоренко.cd -n Степан\ Нечепоренко.cn
```

### Generate

```bash
python3 -m continental generate -d Степан\ Нечепоренко.cd -n Степан\ Нечепоренко.cn -l 1000
```
