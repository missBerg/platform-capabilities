#!/usr/bin/env python3
"""Generate a PCF `.drawio` diagram from a small JSON spec.

The PCF shape libraries (`pcf-components.xml`, `pcf-icons.xml`) are the single
source of truth for styling: this script *parses* them so generated diagrams can
never drift from the library. You describe a diagram as nodes + edges grouped
into lanes; the script lays them out on a deterministic grid and emits valid
uncompressed Draw.io XML that renders with the PCF look anywhere — no library
install required to view it.

Usage:

    python3 scripts/build-diagram.py path/to/diagram.spec.json
    python3 scripts/build-diagram.py --self-check        # validate the libraries

The output `.drawio` is written next to the spec (`foo.spec.json` -> `foo.drawio`).
Render it to an image for visual review with `scripts/render.py`.
"""

from __future__ import annotations

import copy
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# --- layout constants (echo the visual rhythm of the checked-in example) ---
MARGIN = 40            # page edge -> content
LANE_GAP = 90          # gap between lanes (perpendicular to flow)
ROW_GAP = 40           # gap between nodes within a lane (along flow)
SECTION_PAD = 24       # inner padding of a section/group container
SECTION_HEADER = 34    # space reserved at the top of a container for its title
TITLE_H = 56           # vertical space reserved for the diagram title
ICON_LABEL_PAD = 26    # extra spacing under an icon for its bottom label
GRID = 10              # coordinate snap
DEFAULT_PAGE_W = 850
DEFAULT_PAGE_H = 1100

# Short edge aliases accepted in specs -> matched against edge stamp slugs.
EDGE_KEYS = ("provides", "depends", "exchanges", "reconciles")

# Icon image style, verbatim from the checked-in example (a bordered PCF tile).
ICON_STYLE = (
    "shape=image;verticalLabelPosition=bottom;verticalAlign=top;imageAspect=0;"
    "aspect=fixed;image={uri};rounded=1;shadow=0;strokeColor=#2E5C9E;"
    "strokeWidth=1.5;align=center;arcSize=8;fontFamily={font};fontSize=12;"
    "fontColor=#1F3A68;fillColor=#E8EEF7;"
)


def slugify(title: str) -> str:
    """'Capability Consumer' -> 'capability-consumer'; '& ' -> 'and'."""
    s = title.lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def fmt(v: float) -> str:
    """Render a coordinate as a grid-snapped integer string."""
    return str(int(round(v)))


@dataclass
class Stamp:
    slug: str
    title: str
    w: float
    h: float
    cells: list  # list[ET.Element] with geometry relative to the stamp origin
    label_index: int
    label_bold: bool
    is_edge: bool


# --------------------------------------------------------------------------- #
# Library parsing (single source of truth)
# --------------------------------------------------------------------------- #
def load_entries(path: Path) -> list:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"<mxlibrary[^>]*>(.*)</mxlibrary>", text, flags=re.DOTALL)
    if not m:
        raise ValueError(f"{path} is not an <mxlibrary> file")
    return json.loads(m.group(1))


def label_cell_index(cells: list) -> int:
    """The label cell is the first cell whose value is non-empty (else cell 0)."""
    for i, c in enumerate(cells):
        if (c.get("value") or "").strip():
            return i
    return 0


def parse_components(path: Path) -> dict:
    """Return {slug: Stamp} for every component/edge in the library."""
    stamps: dict = {}
    for entry in load_entries(path):
        title = entry["title"]
        inner = html.unescape(entry["xml"])          # unescape exactly once
        model = ET.fromstring(inner)                  # <mxGraphModel>
        root = model.find("root")
        cells = [c for c in root.findall("mxCell") if c.get("id") not in ("0", "1")]
        if not cells:
            continue
        li = label_cell_index(cells)
        is_edge = any(c.get("edge") == "1" for c in cells)
        label_bold = "<b>" in (cells[li].get("value") or "")
        slug = slugify(title)
        stamp = Stamp(slug, title, float(entry["w"]), float(entry["h"]),
                      cells, li, label_bold, is_edge)
        stamps[slug] = stamp
        if is_edge:                                   # also register short aliases
            for key in EDGE_KEYS:
                if key in slug:
                    stamps[key] = stamp
                    stamps[f"edge-{key}"] = stamp
    return stamps


def parse_icons(path: Path) -> dict:
    """Return {slug: data-uri}; strip ';base64' so the URI is style-string safe."""
    icons: dict = {}
    for entry in load_entries(path):
        uri = entry["data"].replace(";base64,", ",", 1)
        icons[slugify(entry["title"])] = uri
    return icons


# --------------------------------------------------------------------------- #
# Cell emission
# --------------------------------------------------------------------------- #
def sublabel_color(style: str) -> str:
    """Grey on light fills, pale blue on dark fills (luminance < 160)."""
    m = re.search(r"fillColor=#([0-9A-Fa-f]{6})", style or "")
    if m:
        r, g, b = (int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4))
        if 0.2126 * r + 0.7152 * g + 0.0722 * b < 160:
            return "#D6E0F0"
    return "#4B5563"


def make_label(text: str, sublabel: str | None, bold: bool,
               style: str = "") -> str:
    """Build the HTML label string (ET escapes it once more on serialize)."""
    main = f"<b>{html.escape(text)}</b>" if bold else html.escape(text)
    if sublabel:
        main += (f'<br><font style="font-size: 11px" color="{sublabel_color(style)}">'
                 f'{html.escape(sublabel)}</font>')
    return main


def place_stamp(stamp: Stamp, x: float, y: float, nid: str,
                label: str | None, sublabel: str | None,
                w: float | None = None, h: float | None = None) -> list:
    """Clone a stamp's cells at (x, y); primary cell gets id=nid.

    A `w`/`h` override scales every cell proportionally so multi-cell stamps
    (ports, decorations) keep their relative arrangement.
    """
    sx = (w / stamp.w) if w else 1.0
    sy = (h / stamp.h) if h else 1.0
    out, sub = [], 0
    for i, tmpl in enumerate(stamp.cells):
        cell = copy.deepcopy(tmpl)
        if i == stamp.label_index:
            cid = nid
        else:
            sub += 1
            cid = f"{nid}-{sub}"
        cell.set("id", cid)
        cell.set("parent", "1")
        geo = cell.find("mxGeometry")
        if geo is not None:
            gx = float(geo.get("x", "0")) * sx
            gy = float(geo.get("y", "0")) * sy
            geo.set("x", fmt(x + gx))
            geo.set("y", fmt(y + gy))
            if geo.get("width") is not None:
                geo.set("width", fmt(float(geo.get("width")) * sx))
            if geo.get("height") is not None:
                geo.set("height", fmt(float(geo.get("height")) * sy))
        out.append(cell)
    if label is not None:
        out[stamp.label_index].set("value", make_label(label, sublabel, stamp.label_bold,
                                                     out[stamp.label_index].get("style", "")))
    return out


def make_icon_cell(nid: str, uri: str, x: float, y: float, w: float, h: float,
                   label: str | None, font: str) -> ET.Element:
    cell = ET.Element("mxCell", {
        "id": nid, "parent": "1", "vertex": "1",
        "style": ICON_STYLE.format(uri=uri, font=font),
        "value": html.escape(label) if label else "",
    })
    ET.SubElement(cell, "mxGeometry", {
        "x": fmt(x), "y": fmt(y), "width": fmt(w), "height": fmt(h), "as": "geometry",
    })
    return cell


_SIDE_POINTS = {"left": (0, 0.5), "right": (1, 0.5), "top": (0.5, 0), "bottom": (0.5, 1)}


def make_edge_cell(eid: str, stamp: Stamp, src: str, tgt: str,
                   label: str | None, sketch: bool,
                   label_pos: float | None = None,
                   label_off: float | None = None,
                   exit_side: str | None = None,
                   entry_side: str | None = None,
                   label_off_x: float | None = None) -> ET.Element:
    cell = copy.deepcopy(stamp.cells[0])
    cell.set("id", eid)
    cell.set("parent", "1")
    cell.set("edge", "1")
    cell.set("source", src)
    cell.set("target", tgt)
    style = "edgeStyle=orthogonalEdgeStyle;" + (cell.get("style") or "")
    style += "curved=1;"
    if sketch:
        style += "sketch=1;curveFitting=1;jiggle=2;"
    if exit_side:
        ex, ey = _SIDE_POINTS[exit_side]
        style += f"exitX={ex};exitY={ey};exitDx=0;exitDy=0;"
    if entry_side:
        ex, ey = _SIDE_POINTS[entry_side]
        style += f"entryX={ex};entryY={ey};entryDx=0;entryDy=0;"
    cell.set("style", style)
    if label:
        cell.set("value", html.escape(label))
    geo = cell.find("mxGeometry")
    if geo is not None:                               # drop sample endpoints
        for pt in list(geo.findall("mxPoint")):
            geo.remove(pt)
        if label_pos is not None:                     # slide label along edge
            geo.set("relative", "1")
            geo.set("x", str(label_pos))
        if label_off is not None or label_off_x is not None:
            # Lift the label off the line. Offsets are page axes, not edge
            # axes: labelOffset moves vertically (use on horizontal edges),
            # labelOffsetX moves horizontally (use on vertical edges).
            geo.set("relative", "1")
            ET.SubElement(geo, "mxPoint",
                          {"x": fmt(label_off_x or 0), "y": fmt(label_off or 0), "as": "offset"})
    return cell


def make_container(cid: str, stamp: Stamp, x: float, y: float, w: float, h: float,
                   label: str) -> ET.Element:
    base = stamp.cells[stamp.label_index]
    cell = ET.Element("mxCell", {
        "id": cid, "parent": "1", "vertex": "1",
        "style": base.get("style") or "",
        "value": make_label(label, None, "<b>" in (base.get("value") or "")),
    })
    ET.SubElement(cell, "mxGeometry", {
        "x": fmt(x), "y": fmt(y), "width": fmt(w), "height": fmt(h), "as": "geometry",
    })
    return cell


def make_title(text: str) -> ET.Element:
    cell = ET.Element("mxCell", {
        "id": "pcf-title", "parent": "1", "vertex": "1",
        "style": ("text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;"
                  "rounded=0;fontColor=#1F3A68;fontFamily=Helvetica;fontSize=18;"
                  "fontStyle=1;spacingLeft=4;"),
        "value": html.escape(text),
    })
    ET.SubElement(cell, "mxGeometry", {
        "x": fmt(MARGIN), "y": "16", "width": "420", "height": "32", "as": "geometry",
    })
    return cell


# --------------------------------------------------------------------------- #
# Spec validation + layout
# --------------------------------------------------------------------------- #
_RESERVED = re.compile(r".*-(\d+|icon)$")


def validate_spec(spec: dict, stamps: dict, icons: dict) -> None:
    ids: set = set()
    for n in spec.get("nodes", []):
        nid = n.get("id")
        if not nid:
            raise ValueError("every node needs an id")
        if nid in ids:
            raise ValueError(f"duplicate node id: {nid}")
        if _RESERVED.match(nid):
            raise ValueError(f"node id {nid!r} clashes with a reserved suffix "
                             "(-<number> / -icon); rename it")
        ids.add(nid)
        ntype = n.get("type", "rectangle-blue-light")
        if ntype == "icon":
            if slugify(n.get("icon", "")) not in icons:
                raise ValueError(f"unknown icon: {n.get('icon')!r}")
        elif ntype == "spacer":
            pass                                      # invisible layout filler
        elif ntype not in stamps:
            raise ValueError(f"unknown node type: {ntype!r}")
        if n.get("icon") and ntype != "icon":
            badge = slugify(n["icon"])
            if n.get("iconColor") == "yellow":
                badge += "-yellow"
            if badge not in icons:
                raise ValueError(f"unknown badge icon: {n['icon']!r}")
    for e in spec.get("edges", []):
        for end in ("source", "target"):
            if e.get(end) not in ids:
                raise ValueError(f"edge {end} {e.get(end)!r} is not a node id")
        etype = e.get("type", "provides")
        if etype not in stamps:
            raise ValueError(f"unknown edge type: {etype!r}")
        for side in ("exit", "entry"):
            v = e.get(side)
            if v is not None and v not in ("left", "right", "top", "bottom"):
                raise ValueError(f"edge {side} must be left/right/top/bottom, got {v!r}")


def node_size(n: dict, stamps: dict) -> tuple:
    ntype = n.get("type", "rectangle-blue-light")
    if ntype == "icon":
        return float(n.get("w", 48)), float(n.get("h", 48))
    if ntype == "spacer":
        return float(n.get("w", 20)), float(n.get("h", 20))
    st = stamps[n["type"]]
    return float(n.get("w", st.w)), float(n.get("h", st.h))


def lane_of(n: dict) -> str:
    return str(n.get("lane", "Main"))


def layout(spec: dict, stamps: dict) -> dict:
    """Assign each node an absolute (x, y, w, h). Returns {id: rect}."""
    nodes = spec.get("nodes", [])
    direction = spec.get("direction", "LR")
    lane_gap = spec.get("laneGap", LANE_GAP)
    row_gap = spec.get("rowGap", ROW_GAP)
    # Reserve room for the title and, when sections are used, for the container
    # header/padding that sits *above* the first row of nodes.
    has_section = any(n.get("section") for n in nodes)
    top = (MARGIN
           + (TITLE_H if spec.get("title") else 0)
           + (SECTION_HEADER + SECTION_PAD if has_section else 0))

    lane_keys: list = []
    for name in spec.get("lanes", []):
        if name not in lane_keys:
            lane_keys.append(name)
    for n in nodes:
        k = lane_of(n)
        if k not in lane_keys:
            lane_keys.append(k)

    by_lane = {k: [n for n in nodes if lane_of(n) == k] for k in lane_keys}
    rects: dict = {}

    if direction == "TB":
        y = top
        for k in lane_keys:
            ns = by_lane[k]
            lane_h = max((node_size(n, stamps)[1] for n in ns), default=0)
            x = MARGIN
            for n in ns:
                w, h = node_size(n, stamps)
                rects[n["id"]] = (x, y + (lane_h - h) / 2, w, h)
                x += w + lane_gap
            y += lane_h + row_gap
    else:  # LR
        x = MARGIN
        for k in lane_keys:
            ns = by_lane[k]
            lane_w = max((node_size(n, stamps)[0] for n in ns), default=0)
            y = top
            for n in ns:
                w, h = node_size(n, stamps)
                rects[n["id"]] = (x + (lane_w - w) / 2, y, w, h)
                eff = h + (ICON_LABEL_PAD if n.get("type") == "icon" and n.get("label") else 0)
                y += eff + row_gap
            x += lane_w + lane_gap
    return rects


def section_boxes(spec: dict, rects: dict) -> list:
    """Compute (id, type, label, x, y, w, h) for each declared section."""
    groups: dict = {}
    for n in spec.get("nodes", []):
        s = n.get("section")
        if s:
            key = (s, n.get("sectionType", "capability-group"))
            groups.setdefault(key, []).append(n["id"])
    boxes = []
    for i, ((label, stype), members) in enumerate(groups.items()):
        xs = [rects[m] for m in members]
        minx = min(r[0] for r in xs)
        miny = min(r[1] for r in xs)
        maxx = max(r[0] + r[2] for r in xs)
        maxy = max(r[1] + r[3] for r in xs)
        bx = minx - SECTION_PAD
        by = miny - SECTION_PAD - SECTION_HEADER
        bw = (maxx - minx) + 2 * SECTION_PAD
        bh = (maxy - miny) + 2 * SECTION_PAD + SECTION_HEADER
        boxes.append((f"pcf-section-{i}", stype, label, bx, by, bw, bh))
    return boxes


# --------------------------------------------------------------------------- #
# Assembly
# --------------------------------------------------------------------------- #
def generate(spec: dict) -> str:
    flavour = spec.get("flavour", "clean")
    sketch = flavour == "sketch"
    comp = REPO / ("pcf-components-sketch.xml" if sketch else "pcf-components.xml")
    icon = REPO / ("pcf-icons-sketch.xml" if sketch else "pcf-icons.xml")
    stamps = parse_components(comp)
    icons = parse_icons(icon)
    font = "Comic Sans MS" if sketch else "Helvetica"

    validate_spec(spec, stamps, icons)
    rects = layout(spec, stamps)

    cells: list = []
    if spec.get("title"):
        cells.append(make_title(spec["title"]))
    # containers first (behind nodes)
    for cid, stype, label, x, y, w, h in section_boxes(spec, rects):
        cells.append(make_container(cid, stamps[stype], x, y, w, h, label))
    # nodes
    for n in spec["nodes"]:
        nid = n["id"]
        x, y, w, h = rects[nid]
        if n.get("type") == "spacer":                  # occupies grid space only
            continue
        if n.get("type") == "icon":
            uri = icons[slugify(n["icon"])]
            cells.append(make_icon_cell(nid, uri, x, y, w, h, n.get("label"), font))
        else:
            cells.extend(place_stamp(stamps[n["type"]], x, y, nid,
                                     n.get("label"), n.get("sublabel"),
                                     n.get("w"), n.get("h")))
            if n.get("icon"):                          # corner badge
                badge = slugify(n["icon"]) + ("-yellow" if n.get("iconColor") == "yellow" else "")
                cells.append(make_icon_cell(f"{nid}-icon", icons[badge],
                                            x - 6, y - 14, 28, 28, None, font))
    # edges last
    for i, e in enumerate(spec.get("edges", [])):
        cells.append(make_edge_cell(f"pcf-edge-{i}", stamps[e.get("type", "provides")],
                                    e["source"], e["target"], e.get("label"), sketch,
                                    e.get("labelPosition"), e.get("labelOffset"),
                                    e.get("exit"), e.get("entry"),
                                    e.get("labelOffsetX")))

    # page size to fit content
    maxx = max((float(c.find("mxGeometry").get("x", "0")) + float(c.find("mxGeometry").get("width", "0"))
                for c in cells if c.find("mxGeometry") is not None), default=DEFAULT_PAGE_W)
    maxy = max((float(c.find("mxGeometry").get("y", "0")) + float(c.find("mxGeometry").get("height", "0"))
                for c in cells if c.find("mxGeometry") is not None), default=DEFAULT_PAGE_H)
    page_w = max(DEFAULT_PAGE_W, int((maxx + MARGIN) // GRID + 1) * GRID)
    page_h = max(DEFAULT_PAGE_H, int((maxy + MARGIN) // GRID + 1) * GRID)

    body = "\n".join("        " + ET.tostring(c, encoding="unicode") for c in cells)
    name = spec.get("title", "PCF Diagram")
    return (
        '<mxfile host="app.diagrams.net">\n'
        f'  <diagram name="{html.escape(name)}" id="pcf-generated">\n'
        f'    <mxGraphModel dx="1422" dy="800" grid="1" gridSize="{GRID}" guides="1" '
        'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
        f'pageWidth="{page_w}" pageHeight="{page_h}" math="0" shadow="0">\n'
        "      <root>\n"
        '        <mxCell id="0" />\n'
        '        <mxCell id="1" parent="0" />\n'
        f"{body}\n"
        "      </root>\n"
        "    </mxGraphModel>\n"
        "  </diagram>\n"
        "</mxfile>\n"
    )


def self_check() -> int:
    """Parse both flavours of both libraries and report stamp/label health."""
    ok = True
    for comp in ("pcf-components.xml", "pcf-components-sketch.xml"):
        stamps = parse_components(REPO / comp)
        uniq = {s.slug: s for s in stamps.values()}
        edges = [s for s in uniq.values() if s.is_edge]
        print(f"{comp}: {len(uniq)} stamps ({len(edges)} edges)")
        for s in uniq.values():
            if not s.cells:
                print(f"  !! {s.slug}: no cells"); ok = False
    for icon in ("pcf-icons.xml", "pcf-icons-sketch.xml"):
        icons = parse_icons(REPO / icon)
        print(f"{icon}: {len(icons)} icons")
        bad = [k for k, v in icons.items() if not v.startswith("data:image/svg+xml,")]
        if bad:
            print(f"  !! malformed data-uri: {bad}"); ok = False
    return 0 if ok else 1


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "--self-check":
        return self_check()
    spec_path = Path(args[0])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    xml = generate(spec)
    stem = spec_path.name
    for suffix in (".spec.json", ".json"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    out = spec_path.with_name(stem + ".drawio")
    out.write_text(xml, encoding="utf-8")
    print(f"wrote {out.relative_to(REPO) if out.is_relative_to(REPO) else out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
