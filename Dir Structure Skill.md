# DataCamp Course → Repo Structure (reusable skill)

A repeatable recipe for turning any DataCamp course into a study repo like this one: a
`Course Structure.md` syllabus map plus a `lessons/` tree of per-video **topics**, each with notes,
generated charts, and a runnable exercises notebook.

Give this file to an assistant (or follow it yourself) and point it at a course URL.

---

## 0. Prerequisites

- **uv** project (`uv init`), Python pinned via `.python-version`.
- Dependencies for notes/charts/notebooks:
  ```
  uv add pandas matplotlib plotly jupyterlab
  brew install ta-lib && uv add ta-lib   # TA-Lib needs its native C lib first
  uv add bt                              # bt pulls in ffn/yfinance; bt.get needs network
  ```
  (Swap in whatever libraries the course actually teaches.)
- Put the course's data files under `course materials/data/` and any PDFs under `course materials/`.
- The scaffolder `new_lesson.py` (see this repo) creates the Chapter/Topic dirs and notebook stubs.

## 1. Build `Course Structure.md` (the syllabus map)

**Source:** the course landing page, `https://www.datacamp.com/courses/<course-slug>`, and the
per-exercise campus pages, `https://campus.datacamp.com/courses/<course-slug>/<chapter-slug>?ex=<n>`.

1. Fetch the landing page and extract **every chapter** and, under each, **every exercise** in order
   with its **title** and **XP**.
2. Determine each exercise's **type**. Types: `Video`, `Multiple choice`, `Coding`, `Matching`.
   - Heuristic (fast, ~90% right): the first 50-XP exercise of each section is a **Video**; other
     50-XP "Understand…"/"The concept of…" items are **Multiple choice**; 100-XP items are
     **Coding**.
   - **Verify the ambiguous ones** by fetching that exercise page and checking the interaction type
     (a `VideoObject` / "Show Transcripts" ⇒ Video; a 100-XP that's actually a quiz/drag ⇒ Multiple
     choice/Matching). Don't trust the heuristic on 100-XP oddballs or mid-chapter 50-XP items — a
     mis-tagged video shifts the whole topic numbering (this happened here with ex 5).
3. Write `Course Structure.md`:
   - One `##` section per chapter, heading linked to its `lessons/` folder (URL-encode spaces as
     `%20`).
   - A table per chapter: `| # | Exercise | XP | Type |`.
   - Annotate each **Video** row with the topic it maps to: `Video → Topic K` (K = sequential video
     index within the chapter, see §2).
   - A short "Themes by chapter" summary at the end.

Find the campus **chapter slugs** from the landing page (they look like `trading-basics-1`,
`technical-indicators`, `performance-evaluation-4` — numbering is inconsistent, so confirm each by
fetching `?ex=1`).

## 2. Map the syllabus to a `lessons/` tree

**Convention:** only **video** exercises become folders. A video defines a **section** = the run of
exercises from that video until the next video.

```
lessons/
└── Chapter<C> - <Chapter Name>/          # one per chapter
    └── Topic <K> - <Video Title>/        # one per video; K = 1,2,3… within the chapter
        ├── Notes.md                      # video summary + code + embedded chart(s)
        ├── Exercises.ipynb               # setup + examples + this section's coding exercises
        └── *.png                         # charts generated from course materials/data
```

- **Topic numbering (K)** is sequential per chapter over the videos only — *not* the course exercise
  number. Example: a chapter whose videos are course-exercises 1/4/8/12 → Topics 1/2/3/4.
- Directory names are human-readable ("Chapter1 - …", "Topic 2 - …"); strip path-hostile characters
  (`:` `/` `\`) from titles.

Scaffold it (don't hand-create dirs — keeps names/numbering consistent):
```
uv run new_lesson.py
```
It prompts for chapter number+name, then each topic (video) title and that topic's coding exercises
(`N. Title`), and writes each `Topic` dir with a `Notes.md` stub and an `Exercises.ipynb` (title +
setup cell + a "Coding exercises in this section" block, one description+`script.py` placeholder per
coding exercise). Re-running an existing chapter appends topics and continues numbering; it never
overwrites.

## 3. Fill each topic's `Notes.md`

Fetch the video page (`?ex=<video-n>`) and compile a **combined summary of the slide lecture** — the
verbatim spoken transcript lives in the player and usually isn't extractable, so summarize the slide
content instead. Structure each `Notes.md`:

- One-line provenance note (summary of the lecture; figures generated from local CSVs, not slides).
- **Summary**, **Key concepts** (definitions, threshold tables), **Formulas** where relevant.
- **Code examples** in the course's idiom (the libraries it teaches).
- **Figures** — embed the generated PNG(s) with a caption (see §4).

## 4. Generate charts from the local data

Write a throwaway script that reads `course materials/data/*.csv`, computes the topic's indicator
with the **real library the course teaches** (e.g. TA-Lib), runs any backtest with the real
framework (e.g. **bt**, fed the **local CSVs** so it's offline + deterministic — don't rely on
`bt.get`'s network), saves a PNG into the topic folder, and embed it in `Notes.md`.

Reusable snippets: indicator on a price series, price+indicator subplots, an equity curve, an
underwater/drawdown plot, a return histogram, a metrics bar chart. Verify a couple by actually
opening the PNGs.

## 5. Populate `Exercises.ipynb`

Each notebook has: a **title** cell (link to the exercise), a **setup** cell, a few **runnable
example** cells, then the **"Coding exercises in this section"** block.

**Setup cell (critical):** notebooks run with cwd = their own deeply-nested folder, *not* the repo
root. Locate data by walking up:
```python
from pathlib import Path
import pandas as pd, matplotlib.pyplot as plt
DATA = next(p / "course materials" / "data"
            for p in [Path.cwd(), *Path.cwd().parents]
            if (p / "course materials" / "data").is_dir())
def load(name): return pd.read_csv(DATA / name, index_col="Date", parse_dates=True)
```

**Coding-exercise cells:** for each coding exercise in the section, fetch its page and add a markdown
cell (the **description/instructions**) and a code cell (the **`script.py`** editor contents,
**keeping the blanks `____`**). Prompt the fetch to "return the exact script.py, do not fill blanks".

> **Verbatim-or-placeholder rule (important):** the fetch tool returns full `script.py` cleanly only
> for simple single-step exercises. Multi-step exercises come back truncated or with *guessed* code.
> Use the verbatim `script.py` only when the fetch is clearly complete (has the `____` blanks and
> matches the instruction steps). Otherwise insert the description + a placeholder cell
> (`# paste script.py from the DataCamp editor`). **Never** commit fabricated/guessed exercise code.

## Conventions & gotchas

- **Only videos get folders**; MC/matching/coding exercises live *inside* a video topic's notebook.
- **Section = video → next video.** Get this right; a mis-tagged video (§1.2) shifts every topic
  number and moves coding exercises between topics.
- **Robust data path** in every notebook (walk-up, §5) — never a fixed relative path.
- **TA-Lib** needs `brew install ta-lib` before `uv add ta-lib`. **bt** needs network for `bt.get`;
  feed it local CSVs instead.
- **Notebook cell ids**: give cells an `id` (nbformat 5+ warns otherwise).
- **Exercise starter cells contain `____`** and won't execute as-is — that's intended; validate the
  notebook *structure* (nbformat read), and only execute the setup/example cells.
- Generate at scale with a small `nbformat`/`matplotlib` script rather than by hand; keep those
  generator scripts in a scratch dir, not the repo.

## Reuse checklist

1. `uv init`; add deps (§0); drop data into `course materials/data/`.
2. Fetch syllabus → write `Course Structure.md`; verify video/type tagging (§1).
3. `uv run new_lesson.py` per chapter → Chapter/Topic dirs (§2).
4. Per topic: `Notes.md` from the video (§3) + generated chart (§4).
5. Per topic notebook: setup + examples + coding exercises via the verbatim-or-placeholder rule (§5).
6. Keep `CLAUDE.md` in sync with the layout; commit per logical step.
