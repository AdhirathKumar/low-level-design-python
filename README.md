# Low Level Design in Python

My notes and runnable Python examples from working through a 10-week Low Level Design (LLD) roadmap: OOP fundamentals, design patterns, supporting data structures, and classic LLD interview problems.

## Start here

| File | What it is |
|------|------------|
| [00-Intro-to-LLD.md](00-Intro-to-LLD.md) | What LLD is, why interviewers ask it, and how machine coding rounds differ |
| [00-Roadmap.md](00-Roadmap.md) | The general roadmap: phases, weeks and all 58 topics |
| [00-Roadmap-Python.md](00-Roadmap-Python.md) | The same roadmap with Python idioms and FastAPI connections for each topic. **Progress is tracked here.** |

## How to use this repo

Everyone is welcome to learn from it. Every topic has its own folder, and the files are numbered in the order to use them:

1. **`1-notes.md`:** read the notes.
2. **`2-example.py`:** run the example and change things to see what breaks.
3. **`3-exercises.md`:** do the four exercises without looking back. Write your answers in the topic's `practice/` folder.
4. **`4-solutions.py`:** check the solutions only after you've finished.

`practice/` folders are git-ignored, so if you clone or fork this repo, your attempts stay out of your commits too.

## Structure

Each phase gets its own folder once I start it, and each topic gets a numbered folder inside it:

```
01-OOP-Fundamentals/
  01-encapsulation/
    1-notes.md       # notes
    2-example.py     # runnable example
    3-exercises.md   # 4 exercises: spot the bug, refactor, build, explain aloud
    4-solutions.py   # runnable solutions and model answers
    practice/        # your own attempts (git-ignored)
  02-abstraction/
    ...
```

A topic is ticked off in the roadmap only after all four exercises are done without looking at the solutions.

| Phase | Folder | Status |
|-------|--------|--------|
| 1 — OOP Fundamentals | [01-OOP-Fundamentals](01-OOP-Fundamentals/) | In progress |
| 2 — Design Patterns | — | Not started |
| 3 — Supporting Data Structures | — | Not started |
| 4 — LLD Problems | — | Not started |

## Running the examples

The repo is a [uv](https://docs.astral.sh/uv/) project pinned to Python 3.13. Set it up once from the repo root:

```bash
uv sync
```

Then run any file from anywhere inside the repo with `uv run`, which uses the project's `.venv` automatically:

```bash
cd 01-OOP-Fundamentals/01-encapsulation
uv run python 2-example.py
```

Examples use only the standard library (Python 3.10+). Pydantic is installed only to run the comparison snippets in the notes.

The files are run directly, not imported, so names like `2-example.py` work fine.

## License

[MIT](LICENSE): free to use, copy and adapt, with credit.
