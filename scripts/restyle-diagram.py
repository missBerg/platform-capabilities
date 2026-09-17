#!/usr/bin/env python3
"""Restyle a .drawio file in place for the paper set (idempotent, stdlib only).

    python3 scripts/restyle-diagram.py diagrams/foo.drawio [more.drawio ...]

Applies the print rules from diagrams/REVIEW-2026-09-17.md without touching
geometry, so hand-polished layouts survive:
  - sketch flavour -> clean: drop sketch/jiggle/curveFitting/fillStyle tokens,
    Comic Sans MS -> Helvetica (curved edges are kept)
  - fonts: vertex labels 12 -> 14 px, sublabels and edge labels 11 -> 12 px,
    section headers 13 -> 14 px
  - edge stroke 1.5 -> 2 px
  - sublabel grey #6B7280 -> #4B5563, gold tag fill #B5915A -> #8A6A38
"""
import re
import sys
from pathlib import Path

TOKENS = re.compile(r"(sketch=1|curveFitting=1|jiggle=2|fillStyle=solid);")


def restyle_style(style: str, is_edge: bool) -> str:
    style = TOKENS.sub("", style)
    style = style.replace("fontFamily=Comic Sans MS", "fontFamily=Helvetica")
    style = style.replace("fillColor=#B5915A", "fillColor=#8A6A38")
    if is_edge:
        style = re.sub(r"fontSize=11\b", "fontSize=12", style)
        style = re.sub(r"strokeWidth=1(\.5)?;", "strokeWidth=2;", style)
    else:
        style = re.sub(r"fontSize=1[23]\b", "fontSize=14", style)
        style = re.sub(r"fontSize=11\b", "fontSize=12", style)
    return style


def restyle_value(value: str) -> str:
    value = value.replace("font-size: 11px", "font-size: 12px")
    return value.replace("#6B7280", "#4B5563")


def restyle(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    def cell(m: re.Match) -> str:
        tag = m.group(0)
        is_edge = 'edge="1"' in tag
        tag = re.sub(r'style="([^"]*)"', lambda s: f'style="{restyle_style(s.group(1), is_edge)}"', tag)
        tag = re.sub(r'value="([^"]*)"', lambda v: f'value="{restyle_value(v.group(1))}"', tag)
        return tag

    new = re.sub(r"<mxCell\b[^>]*>", cell, text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        print(f"restyled {path}")
    else:
        print(f"unchanged {path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    for arg in sys.argv[1:]:
        restyle(Path(arg))
