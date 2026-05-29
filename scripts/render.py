#!/usr/bin/env python3
"""Render a `.drawio` file to an image using the draw.io desktop CLI.

This is the verification half of the diagram workflow: generate with
`build-diagram.py`, then render here and *look at the result* to catch overlaps,
cut-off labels, or routing problems before committing.

    python3 scripts/render.py diagrams/foo.drawio                # -> foo.png
    python3 scripts/render.py diagrams/foo.drawio --format svg   # -> foo.svg
    python3 scripts/render.py diagrams/foo.drawio --scale 3

Requires the draw.io desktop app (`brew install --cask drawio`). The binary is
located automatically; override with the DRAWIO_BIN environment variable.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

CANDIDATES = [
    "/Applications/draw.io.app/Contents/MacOS/draw.io",
    "/Applications/drawio.app/Contents/MacOS/drawio",
]


def find_binary() -> str | None:
    env = os.environ.get("DRAWIO_BIN")
    if env and Path(env).exists():
        return env
    for c in CANDIDATES:
        if Path(c).exists():
            return c
    return shutil.which("drawio") or shutil.which("draw.io")


def export(binary: str, infile: Path, fmt: str, scale: str, border: str) -> int:
    out = infile.with_suffix(f".{fmt}")
    cmd = [binary, "--export", "--format", fmt, "--scale", scale,
           "--border", border, "--output", str(out), str(infile)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout + proc.stderr)
        print(f"draw.io export failed (exit {proc.returncode}). "
              "Headless runs may need a display; try opening the app once.")
        return proc.returncode
    print(f"wrote {out}")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    infile = Path(args[0])
    if not infile.exists():
        print(f"no such file: {infile}")
        return 1
    fmt, scale, border = "png", "2", "20"
    i = 1
    while i < len(args):
        if args[i] == "--format":
            fmt = args[i + 1]; i += 2
        elif args[i] == "--scale":
            scale = args[i + 1]; i += 2
        elif args[i] == "--border":
            border = args[i + 1]; i += 2
        else:
            print(f"unknown argument: {args[i]}"); return 2
    binary = find_binary()
    if not binary:
        print("draw.io not found. Install it with:  brew install --cask drawio\n"
              "or set DRAWIO_BIN to the executable path.")
        return 1
    return export(binary, infile, fmt, scale, border)


if __name__ == "__main__":
    raise SystemExit(main())
