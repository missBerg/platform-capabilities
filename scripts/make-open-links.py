#!/usr/bin/env python3
"""Generate diagrams.net deep links that open a checked-in diagram with the
PCF shape libraries pre-loaded in the left panel.

A `.drawio` file already carries its styles inline, so it always *renders*
with the PCF look. What a file cannot store is which custom libraries are
open in the editor — that is app state. diagrams.net solves this with the
`clibs` URL parameter, so these links open the diagram *and* attach the
libraries in one click.

Run from anywhere:

    python3 scripts/make-open-links.py

Prints a Markdown table to stdout (used to keep the README links in sync).
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parent.parent

# GitHub owner/repo and branch the raw files are served from.
SLUG = "missBerg/platform-capabilities"
BRANCH = "main"
RAW = f"https://raw.githubusercontent.com/{SLUG}/{BRANCH}"
APP = "https://app.diagrams.net/"

# The four PCF libraries, attached to every link so editors get the full kit.
LIBRARIES = [
    "pcf-components.xml",
    "pcf-components-sketch.xml",
    "pcf-icons.xml",
    "pcf-icons-sketch.xml",
]


def clibs_param() -> str:
    """Build the `clibs` value: U<encoded-url> entries joined by ';'."""
    entries = [f"U{quote(f'{RAW}/{lib}', safe='')}" for lib in LIBRARIES]
    return ";".join(entries)


def open_link(diagram_rel: str) -> str:
    """A link that opens `diagram_rel` from raw GitHub with libraries loaded."""
    diagram_url = f"{RAW}/{quote(diagram_rel)}"
    return f"{APP}?clibs={clibs_param()}#U{quote(diagram_url, safe='')}"


def main() -> int:
    diagrams = sorted((REPO / "diagrams").glob("*.drawio"))
    if not diagrams:
        print("no .drawio files under diagrams/")
        return 1
    print("| Diagram | Open in diagrams.net (libraries pre-loaded) |")
    print("| ------- | -------------------------------------------- |")
    for d in diagrams:
        rel = f"diagrams/{d.name}"
        print(f"| `{d.name}` | [Open]({open_link(rel)}) |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
