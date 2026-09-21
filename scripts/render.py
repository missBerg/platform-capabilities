#!/usr/bin/env python3
"""Render a `.drawio` file to an image using the draw.io desktop CLI.

This is the verification half of the diagram workflow: generate with
`build-diagram.py`, then render here and *look at the result* to catch overlaps,
cut-off labels, or routing problems before committing.

    python3 scripts/render.py diagrams/foo.drawio                # -> foo.png
    python3 scripts/render.py diagrams/foo.drawio --format svg   # -> foo.svg
    python3 scripts/render.py diagrams/foo.drawio --scale 3
    python3 scripts/render.py diagrams/foo.drawio --transparent --output out/fig.png

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


PDF_COLUMN_PT = 468  # US Letter, 1in margins: the width a figure is scaled to


def pdf_report(infile: Path) -> None:
    """Print the effective point size of the smallest font at PDF column width."""
    import re
    import xml.etree.ElementTree as ET
    root = ET.parse(infile).getroot()
    xs, fonts = [], set()
    for c in root.iter("mxCell"):
        g = c.find("mxGeometry")
        if c.get("vertex") != "1" or g is None or not c.get("value"):
            continue
        x, w = float(g.get("x", 0)), float(g.get("width", 0))
        xs += [x, x + w]
        m = re.search(r"fontSize=(\d+)", c.get("style", ""))
        if m:
            fonts.add(int(m.group(1)))
        fonts.update(int(f) for f in re.findall(r"font-size: ?(\d+)px", c.get("value")))
    if not xs or not fonts:
        return
    width = max(xs) - min(xs)
    pt = PDF_COLUMN_PT / width * min(fonts)
    flag = "" if pt >= 7 else "  <-- below 7pt, widen fonts or narrow the canvas"
    print(f"pdf-check: width {width:.0f} units, smallest font {min(fonts)}px -> {pt:.1f}pt at {PDF_COLUMN_PT}pt column{flag}")


def export(binary: str, infile: Path, fmt: str, scale: str, border: str,
           transparent: bool = False, out: Path | None = None) -> int:
    out = out or infile.with_suffix(f".{fmt}")
    cmd = [binary, "--export", "--format", fmt, "--scale", scale,
           "--border", border, "--output", str(out)]
    if transparent and fmt == "png":
        cmd.append("--transparent")
    cmd.append(str(infile))
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
    pdf_check, transparent, out = False, False, None
    i = 1
    while i < len(args):
        if args[i] == "--format":
            fmt = args[i + 1]; i += 2
        elif args[i] == "--scale":
            scale = args[i + 1]; i += 2
        elif args[i] == "--border":
            border = args[i + 1]; i += 2
        elif args[i] == "--pdf-check":
            pdf_check = True; i += 1
        elif args[i] == "--transparent":
            transparent = True; i += 1
        elif args[i] == "--output":
            out = Path(args[i + 1]); i += 2
        else:
            print(f"unknown argument: {args[i]}"); return 2
    if pdf_check:
        pdf_report(infile)
    binary = find_binary()
    if not binary:
        print("draw.io not found. Install it with:  brew install --cask drawio\n"
              "or set DRAWIO_BIN to the executable path.")
        return 1
    return export(binary, infile, fmt, scale, border, transparent, out)


if __name__ == "__main__":
    raise SystemExit(main())
