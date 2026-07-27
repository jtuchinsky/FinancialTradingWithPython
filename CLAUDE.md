# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Workspace for following DataCamp's **Financial Trading with Python** course. It is a
`uv`-initialized Python project. Course work lives under `lessons/`, and the source material is in
`course materials/`.

## Lessons layout

Course content is mirrored under `lessons/` as **lessons** (chapters) containing **sublessons**
(exercises). Both levels use a zero-padded, ordered `NN-slug` directory name and carry a `README.md`
whose heading is `# N. Title`:

```
lessons/
└── 01-trading-basics/            # lesson (chapter)
    ├── README.md                 # "# 1. Trading Basics"
    ├── 01-what-is-financial-trading/
    │   └── README.md             # "# 1. What is financial trading"
    └── 03-plot-a-time-series-line-chart/
        └── README.md
```

### Adding a lesson or sublesson

Use the interactive helper — don't hand-create the directories, so numbering and slugs stay
consistent:

```
uv run new_lesson.py
```

It prompts for a lesson number + title, then sublesson titles (one per line, blank to finish), and
creates `lessons/<NN>-<slug>/README.md` plus a `<MM>-<slug>/README.md` per sublesson. Re-running with
an **existing** lesson number appends new sublessons, continuing the numbering from the highest
existing prefix (it never overwrites an existing `README.md`).

## Toolchain

Managed with [`uv`](https://docs.astral.sh/uv/) (v0.11.x), Python pinned to 3.11 via `.python-version`.
Dependencies live in `pyproject.toml` (`[project].dependencies`, currently empty) — there is no
`uv.lock` yet; the first `uv add` / `uv sync` creates one.

## Commands

- Run: `uv run main.py` (or `uv run python main.py`)
- Add a dependency: `uv add <package>` — prefer this over editing `pyproject.toml` by hand; it
  resolves and writes `uv.lock`
- Sync the environment from the lockfile: `uv sync`
- Ad-hoc Python in the project env: `uv run python -c "..."`

No test runner, linter, or formatter is configured yet. If adding tests, `uv add --dev pytest` and
run with `uv run pytest` (a single test: `uv run pytest path/to/test.py::test_name`).