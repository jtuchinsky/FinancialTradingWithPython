"""Interactively scaffold a lesson under lessons/.

Creates:
    lessons/<NN>-<slug>/README.md
    lessons/<NN>-<slug>/<MM>-<slug>/README.md   (one per sublesson you enter)

Both lessons and sublessons use a zero-padded, ordered prefix (e.g.
01-trading-basics/03-plot-a-candlestick-chart) to match the course structure.
Re-running for an existing lesson number appends new sublessons, continuing the
numbering.

Run with:  uv run new_lesson.py   (or: python new_lesson.py)
"""

import re
from pathlib import Path

LESSONS_DIR = Path(__file__).parent / "lessons"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


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


def prompt_sublessons() -> list[str]:
    titles: list[str] = []
    print("Enter sublesson titles one per line (blank line to finish):")
    while True:
        title = input("  Sublesson: ").strip()
        if not title:
            break
        titles.append(title)
    return titles


def find_lesson_dir(number: int) -> Path | None:
    """Return an existing lessons/<NN>-* dir for this number, if any."""
    prefix = f"{number:02d}-"
    if LESSONS_DIR.exists():
        for child in LESSONS_DIR.iterdir():
            if child.is_dir() and child.name.startswith(prefix):
                return child
    return None


def next_index(lesson_dir: Path) -> int:
    """Highest existing NN- prefix inside the lesson dir, plus one."""
    highest = 0
    for child in lesson_dir.iterdir():
        m = re.match(r"(\d+)-", child.name)
        if child.is_dir() and m:
            highest = max(highest, int(m.group(1)))
    return highest + 1


def create_lesson(number: int, title: str, sublessons: list[str]) -> None:
    lesson_dir = find_lesson_dir(number)
    if lesson_dir is not None:
        print(f"\n'{lesson_dir}' already exists — adding to it.")
    else:
        lesson_dir = LESSONS_DIR / f"{number:02d}-{slugify(title)}"
    lesson_dir.mkdir(parents=True, exist_ok=True)

    readme = lesson_dir / "README.md"
    if not readme.exists():
        readme.write_text(f"# {number}. {title}\n")

    created = [str(readme.relative_to(LESSONS_DIR.parent))]
    index = next_index(lesson_dir)
    for offset, sub_title in enumerate(sublessons):
        n = index + offset
        sub_dir = lesson_dir / f"{n:02d}-{slugify(sub_title)}"
        sub_dir.mkdir(parents=True, exist_ok=True)
        (sub_dir / "README.md").write_text(f"# {n}. {sub_title}\n")
        created.append(str(sub_dir.relative_to(LESSONS_DIR.parent)) + "/")

    print("\nCreated:")
    for path in created:
        print(f"  {path}")


def main() -> None:
    number = prompt_number("Lesson")
    title = prompt_title("Lesson")
    sublessons = prompt_sublessons()
    create_lesson(number, title, sublessons)


if __name__ == "__main__":
    main()