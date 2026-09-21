#!/usr/bin/env python3
"""Combine per-diagram .drawio files into one multi-tab (multi-page) .drawio.

Each source .drawio is an <mxfile> with a single <diagram> page. draw.io shows
one tab per <diagram>, but it requires the diagram ids to be unique within a
file (the generated ones all share id="pcf-generated"). This script lifts each
source's <diagram> block *verbatim* — preserving the inline PCF styles — assigns
a unique id derived from the filename, keeps the human-readable tab name, and
concatenates the blocks into one <mxfile> in a deterministic, factor-ordered
sequence.

stdlib only. Usage:
    python3 scripts/combine-diagrams.py [--output diagrams/pcf-all.drawio] [INPUT.drawio ...]

With no INPUTs it globs diagrams/*.drawio (excluding the output file).
"""
import argparse
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET

DIAGRAM_RE = re.compile(r"<diagram\b[^>]*>.*?</diagram>", re.DOTALL)
OPEN_TAG_RE = re.compile(r"<diagram\b[^>]*>", re.DOTALL)
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')

# Preferred tab order: paper order (limitations, ecosystem model, contract,
# then the five factors). Files not listed here sort after these, alphabetically.
PREFERRED = [
    "challenge-central-bottleneck",
    "centralized-friction-loop",
    "ecosystem-architecture-lineage",
    "ecosystem-value-exchange",
    "participation-contract",
    "factors-overview",
    "factor-1-defined-contract",
    "factor-2-declarative-inputs",
    "factor-3-encapsulated-dependencies",
    "factor-4-stable-reconciliation",
    "factor-5-operational-evidence",
    "factors-to-outcomes",
]


def order_key(stem):
    try:
        return (0, PREFERRED.index(stem))
    except ValueError:
        return (1, stem)


def extract_diagram(path):
    """Return the <diagram>…</diagram> block with a unique id and preserved name."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = DIAGRAM_RE.search(text)
    if not m:
        sys.exit(f"error: no <diagram> element found in {path}")
    if DIAGRAM_RE.search(text, m.end()):
        sys.exit(f"error: {path} has more than one <diagram>; not supported")
    block = m.group(0)
    stem = os.path.splitext(os.path.basename(path))[0]
    open_tag = OPEN_TAG_RE.search(block).group(0)
    attrs = dict(ATTR_RE.findall(open_tag))
    name = attrs.get("name", stem)  # already XML-escaped in the source
    new_open = f'<diagram id="{stem}" name="{name}">'
    return stem, OPEN_TAG_RE.sub(new_open, block, count=1)


def main():
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="*", help="source .drawio files (default: diagrams/*.drawio)")
    ap.add_argument("--output", default=os.path.join(repo, "diagrams", "pcf-all.drawio"),
                    help="combined multi-tab .drawio (default: diagrams/pcf-all.drawio)")
    args = ap.parse_args()

    out = os.path.abspath(args.output)
    inputs = [os.path.abspath(p) for p in args.inputs]
    if not inputs:
        inputs = [p for p in glob.glob(os.path.join(repo, "diagrams", "*.drawio"))
                  if os.path.abspath(p) != out]

    inputs.sort(key=lambda p: order_key(os.path.splitext(os.path.basename(p))[0]))

    blocks, seen = [], {}
    for path in inputs:
        stem, block = extract_diagram(path)
        if stem in seen:
            sys.exit(f"error: duplicate diagram id {stem!r} from {path}")
        seen[stem] = path
        blocks.append(block)

    body = "\n  ".join(blocks)
    combined = f'<mxfile host="app.diagrams.net">\n  {body}\n</mxfile>\n'

    # Validate well-formedness before writing.
    try:
        ET.fromstring(combined)
    except ET.ParseError as exc:
        sys.exit(f"error: combined output is not well-formed XML: {exc}")

    with open(out, "w", encoding="utf-8") as fh:
        fh.write(combined)

    rel = os.path.relpath(out, repo)
    print(f"Wrote {rel} with {len(blocks)} tabs:")
    for path in inputs:
        print(f"  - {os.path.splitext(os.path.basename(path))[0]}")


if __name__ == "__main__":
    main()
