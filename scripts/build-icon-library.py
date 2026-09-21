#!/usr/bin/env python3
"""Bundle SVG icons in icons/ into Draw.io shape libraries.

Outputs two libraries at the repo root:
  - pcf-icons.xml          (clean SVGs)
  - pcf-icons-sketch.xml   (same SVGs with a roughen filter injected)

Each library is an <mxlibrary> envelope wrapping a JSON array; each
entry uses the `data` field (a base64-encoded SVG data URI) so the
shape is self-contained — no external image hosting required.
"""

from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ICONS_DIR = REPO / "icons"

GROUP_ORDER = ["callouts", "actors", "ops", "status"]
ICON_SIZE = 48

# Each variant produces a recoloured copy of every icon whose SVG contains the
# `source` colour. The base (unvariant) entry is always emitted first.
COLOR_VARIANTS: list[tuple[str, str, str]] = [
    ("Yellow", "#2E5C9E", "#B5915A"),
    ("Blue", "#5A7A5A", "#2E5C9E"),    # green callouts (success, healthy) in PCF blue
    ("Red", "#2E5C9E", "#A85959"),     # blue icons in the callout red (a bad state)
]

ROUGHEN_FILTER = (
    '<defs>'
    '<filter id="rough" x="-10%" y="-10%" width="120%" height="120%">'
    '<feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="7" result="noise"/>'
    '<feDisplacementMap in="SourceGraphic" in2="noise" scale="1.6"/>'
    '</filter>'
    '</defs>'
)


def pretty_title(stem: str) -> str:
    """ai-agent -> AI Agent; scheduled-job -> Scheduled Job."""
    words = stem.split("-")
    out = []
    for w in words:
        if w.lower() in {"ai", "api"}:
            out.append(w.upper())
        else:
            out.append(w.capitalize())
    return " ".join(out)


def collect_svgs() -> list[tuple[str, Path]]:
    """Return (group, path) pairs in stable order."""
    result: list[tuple[str, Path]] = []
    for group in GROUP_ORDER:
        group_dir = ICONS_DIR / group
        if not group_dir.is_dir():
            continue
        for svg in sorted(group_dir.glob("*.svg")):
            result.append((group, svg))
    return result


def to_data_uri(svg_bytes: bytes) -> str:
    b64 = base64.b64encode(svg_bytes).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


def make_entry(svg_bytes: bytes, title: str) -> dict:
    return {
        "data": to_data_uri(svg_bytes),
        "w": ICON_SIZE,
        "h": ICON_SIZE,
        "title": title,
        "aspect": "fixed",
    }


def color_variants(svg_bytes: bytes, base_title: str):
    """Yield (title, svg_bytes) for base + any colour variants that apply."""
    yield base_title, svg_bytes
    text = svg_bytes.decode("utf-8")
    for label, src, dst in COLOR_VARIANTS:
        if src in text:
            variant = text.replace(src, dst).encode("utf-8")
            yield f"{base_title} ({label})", variant


def inject_sketch_filter(svg_bytes: bytes) -> bytes:
    """Wrap inner SVG in a <g filter="url(#rough)"> and add the filter def."""
    text = svg_bytes.decode("utf-8")
    m = re.search(r"(<svg\b[^>]*>)(.*)(</svg>)", text, flags=re.DOTALL)
    if not m:
        raise ValueError("not a well-formed SVG")
    open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
    wrapped = f'{open_tag}{ROUGHEN_FILTER}<g filter="url(#rough)">{inner}</g>{close_tag}'
    return wrapped.encode("utf-8")


def build_library(title: str, transform=None) -> tuple[str, list[dict]]:
    entries: list[dict] = []
    for _group, svg_path in collect_svgs():
        raw = svg_path.read_bytes()
        base_title = pretty_title(svg_path.stem)
        for variant_title, variant_bytes in color_variants(raw, base_title):
            final_bytes = transform(variant_bytes) if transform else variant_bytes
            entries.append(make_entry(final_bytes, variant_title))
    body = json.dumps(entries, separators=(",", ":"))
    xml = f'<mxlibrary title="{title}">{body}</mxlibrary>\n'
    return xml, entries


def main() -> int:
    pairs = collect_svgs()
    if not pairs:
        print("no SVGs found under icons/", file=sys.stderr)
        return 1

    clean_xml, clean_entries = build_library("PCF Working Group — Icons")
    sketch_xml, sketch_entries = build_library(
        "PCF Working Group — Icons (Sketch)", transform=inject_sketch_filter
    )

    clean_path = REPO / "pcf-icons.xml"
    sketch_path = REPO / "pcf-icons-sketch.xml"
    clean_path.write_text(clean_xml, encoding="utf-8")
    sketch_path.write_text(sketch_xml, encoding="utf-8")

    by_group: dict[str, int] = {}
    for group, _ in pairs:
        by_group[group] = by_group.get(group, 0) + 1

    print("Built icon libraries:")
    for g in GROUP_ORDER:
        if g in by_group:
            print(f"  {g:10s} {by_group[g]:3d}")
    print(f"  {'TOTAL':10s} {len(pairs):3d}")
    print()
    print(f"  {clean_path.relative_to(REPO)}  ({clean_path.stat().st_size:,} bytes)")
    print(f"  {sketch_path.relative_to(REPO)}  ({sketch_path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
