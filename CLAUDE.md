# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Workspace for working through DataCamp's **Financial Trading in Python** course. `uv`-managed Python
project. Study notes and runnable exercises live under `lessons/`, the full syllabus is in
[`Course Structure.md`](Course%20Structure.md), and source material (the chapter PDF and price-data
CSVs) is in `course materials/`.

## Lessons layout

`lessons/` is organized by **chapter** and **topic**, with human-readable directory names:

```
lessons/
└── Chapter1 - Trading Basics/                 # one dir per course chapter
    ├── Topic 1 - What is financial trading/   # one dir per *video* exercise
    │   ├── Notes.md          # lecture summary, formulas, talib/bt code, embedded charts
    │   ├── Exercises.ipynb   # runnable talib/bt starter code against the local CSVs
    │   └── *.png             # charts generated from course materials/data
    └── Topic 2 - Financial trading with bt/
        └── ...
```

- A **Topic N** folder exists only for a chapter's **video** exercises, numbered sequentially per
  chapter (e.g. Chapter 2's videos at course-exercises 1/4/8/12 become Topics 1–4). Coding /
  multiple-choice / matching exercises are not scaffolded. `Course Structure.md` lists every exercise
  and marks which are videos (and their Topic number).
- Chart PNGs are generated from the CSVs in `course materials/data/` using **TA-Lib** indicators and
  **bt** backtests, then embedded in each `Notes.md`.

### Adding a chapter or topic

Use the interactive helper so names and numbering stay consistent — don't hand-create the dirs:

```
uv run new_lesson.py
```

It prompts for a chapter number + name, then topic titles (one per line, blank to finish), and
creates `lessons/Chapter<N> - <Name>/Topic <M> - <Title>/` with a `Notes.md` and a starter
`Exercises.ipynb` in each. Re-running with an existing chapter number appends topics, continuing the
numbering (it never overwrites existing files).

## Data & notebooks

- Price data: `course materials/data/{AMZN,GOOG,TSLA}-stock-data.csv` (OHLCV + Adj Close, 2015–2020)
  and `Bitcoin-price-data.csv` (OHLCV, 2016–2020).
- Notebooks run with the kernel's working directory set to the **notebook's own folder** (deeply
  nested under `lessons/`), not the project root. Each `Exercises.ipynb` therefore finds data by
  walking up from `Path.cwd()` to locate `course materials/data/` rather than using a fixed relative
  path — reuse that `load()` helper in new cells instead of hard-coding a path.

## Toolchain

Managed with [`uv`](https://docs.astral.sh/uv/); Python pinned to 3.11 via `.python-version`.
Dependencies (`pyproject.toml`): `pandas`, `matplotlib`, `plotly`, `ta-lib`, `bt`, `jupyterlab`.

- **TA-Lib** needs its native C library installed first: `brew install ta-lib` (the `ta-lib` Python
  wheel links against it).
- **bt** pulls in `ffn`/`yfinance`; `bt.get(...)` downloads from Yahoo Finance and needs network. The
  generated charts and notebooks instead feed `bt` the local CSVs, so they run offline and
  deterministically.

## Commands

- Add a dependency: `uv add <package>` (resolves and writes `uv.lock`)
- Sync the env from the lockfile: `uv sync`
- Launch Jupyter: `uv run jupyter lab`
- Run a notebook headless: `uv run jupyter nbconvert --to notebook --execute "<path>/Exercises.ipynb"`
- Ad-hoc Python in the project env: `uv run python -c "..."`

No test runner, linter, or formatter is configured.