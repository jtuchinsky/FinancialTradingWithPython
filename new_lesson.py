"""Interactively scaffold a chapter/topic under lessons/.

Creates, matching the repo layout:
    lessons/Chapter<N> - <Name>/Topic <M> - <Title>/Notes.md
    lessons/Chapter<N> - <Name>/Topic <M> - <Title>/Exercises.ipynb

Only *video* exercises get a Topic folder (that is the convention here). Re-running
for an existing chapter number appends new topics, continuing the numbering. Existing
files are never overwritten.

Run with:  uv run new_lesson.py   (or: python new_lesson.py)
"""

import json
import re
from pathlib import Path

LESSONS_DIR = Path(__file__).parent / "lessons"

# Setup cell shared by every generated Exercises.ipynb — finds the data folder no
# matter where the kernel runs from (notebooks run from their own nested folder).
SETUP_CELL = '''\
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Locate the project's data folder regardless of where this notebook runs from
DATA = next(p / "course materials" / "data"
            for p in [Path.cwd(), *Path.cwd().parents]
            if (p / "course materials" / "data").is_dir())

def load(name):
    """Load an OHLCV CSV with a parsed DatetimeIndex."""
    return pd.read_csv(DATA / name, index_col="Date", parse_dates=True)
'''


def sanitize(name: str) -> str:
    """Make a title safe for a directory name (drop path-hostile characters)."""
    return re.sub(r"\s+", " ", re.sub(r"[:/\\]", " ", name)).strip()


def prompt_number(label: str) -> int:
    while True:
        raw = input(f"{label} number: ").strip()
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        print("  Please enter a positive whole number.")


def prompt_title(label: str) -> str:
    while True:
        title = input(f"{label} title: ").strip()
        if title:
            return title
        print("  Title cannot be empty.")


def prompt_topics() -> list[str]:
    titles: list[str] = []
    print("Enter topic (video) titles one per line (blank line to finish):")
    while True:
        title = input("  Topic: ").strip()
        if not title:
            break
        titles.append(title)
    return titles


def find_chapter_dir(number: int) -> Path | None:
    """Return an existing 'Chapter<N> - *' dir, if any."""
    prefix = f"Chapter{number} - "
    if LESSONS_DIR.exists():
        for child in LESSONS_DIR.iterdir():
            if child.is_dir() and child.name.startswith(prefix):
                return child
    return None


def next_topic_index(chapter_dir: Path) -> int:
    """Highest existing 'Topic <n> - ' index in the chapter, plus one."""
    highest = 0
    for child in chapter_dir.iterdir():
        m = re.match(r"Topic (\d+) - ", child.name)
        if child.is_dir() and m:
            highest = max(highest, int(m.group(1)))
    return highest + 1


def exercises_notebook(title: str) -> str:
    """Minimal but runnable Exercises.ipynb (title cell + setup cell)."""
    nb = {
        "cells": [
            {"cell_type": "markdown", "id": "title", "metadata": {},
             "source": f"# Exercises — {title}\n\nSee `Notes.md` in this folder for the summary."},
            {"cell_type": "code", "id": "setup", "metadata": {}, "execution_count": None,
             "outputs": [], "source": SETUP_CELL},
            {"cell_type": "code", "id": "work", "metadata": {}, "execution_count": None,
             "outputs": [], "source": "# Your work here\n"},
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return json.dumps(nb, indent=1)


def create(number: int, name: str, topics: list[str]) -> None:
    chapter_dir = find_chapter_dir(number)
    if chapter_dir is not None:
        print(f"\n'{chapter_dir.name}' already exists — adding to it.")
    else:
        chapter_dir = LESSONS_DIR / f"Chapter{number} - {sanitize(name)}"
    chapter_dir.mkdir(parents=True, exist_ok=True)

    created = []
    index = next_topic_index(chapter_dir)
    for offset, topic_title in enumerate(topics):
        m = index + offset
        topic_dir = chapter_dir / f"Topic {m} - {sanitize(topic_title)}"
        topic_dir.mkdir(parents=True, exist_ok=True)

        notes = topic_dir / "Notes.md"
        if not notes.exists():
            notes.write_text(f"# Topic {m} — {topic_title}\n")
            created.append(notes)

        nb = topic_dir / "Exercises.ipynb"
        if not nb.exists():
            nb.write_text(exercises_notebook(topic_title))
            created.append(nb)

    print("\nCreated:")
    if not created:
        print("  (nothing new — files already existed)")
    for path in created:
        print(f"  {path.relative_to(LESSONS_DIR.parent)}")


def main() -> None:
    number = prompt_number("Chapter")
    name = prompt_title("Chapter")
    topics = prompt_topics()
    create(number, name, topics)


if __name__ == "__main__":
    main()