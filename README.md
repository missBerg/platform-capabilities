# Platform Capabilities Framework — Draw.io Library

A Draw.io / diagrams.net shape library for diagramming platform capabilities,
services, ownership, and operational state. It ships a consistent visual
language (the **PCF** palette and "Architects Daughter" sketch font) so
diagrams across a working group look like they came from the same hand.

The library comes in two flavours:

| Flavour    | Components                  | Icons                  |
| ---------- | --------------------------- | ---------------------- |
| **Clean**  | `pcf-components.xml`        | `pcf-icons.xml`        |
| **Sketch** | `pcf-components-sketch.xml` | `pcf-icons-sketch.xml` |

- **Components** — boxes, edges, swimlanes, callouts, and other diagram
  building blocks (Capability, Platform, Service, Decision, Risk/Gap, …).
- **Icons** — 30 self-contained SVG glyphs grouped into `actors`, `callouts`,
  `ops`, and `status`. They embed as base64 data URIs, so no image hosting is
  required.
- **Sketch** variants apply a hand-drawn roughen filter for a whiteboard look.

## Quick start — import a library

Draw.io loads shape libraries from a URL. Use the **raw** GitHub URLs below.

1. Open [app.diagrams.net](https://app.diagrams.net) (or the desktop app).
2. **File → Open Library from → URL…**
3. Paste one of the raw URLs and click **Open**. The shapes appear in a new
   panel on the left.

| Library            | Raw URL                                                                                  |
| ------------------ | ---------------------------------------------------------------------------------------- |
| Components         | `https://raw.githubusercontent.com/missBerg/platform-capabilities/main/pcf-components.xml`        |
| Components (Sketch)| `https://raw.githubusercontent.com/missBerg/platform-capabilities/main/pcf-components-sketch.xml` |
| Icons              | `https://raw.githubusercontent.com/missBerg/platform-capabilities/main/pcf-icons.xml`             |
| Icons (Sketch)     | `https://raw.githubusercontent.com/missBerg/platform-capabilities/main/pcf-icons-sketch.xml`      |

> Prefer a local copy? Download the `.xml` files and use
> **File → Open Library from → Device…** instead.

## Recommended — load everything via the theme config

`pcf-theme.json` registers all four libraries *and* sets the PCF default
styles, colour schemes, preset palette, and sketch font in one shot. This is
the best option for a team: everyone gets the same defaults.

1. In Draw.io: **Extras → Configuration…** (web) or
   **Preferences → Configuration** (desktop).
2. Paste the contents of [`pcf-theme.json`](pcf-theme.json).
3. Click **Apply** and reload. The four PCF libraries auto-load on every
   diagram, and new shapes/edges inherit the PCF style by default.

The font (`Architects Daughter`) is pulled from Google Fonts automatically via
the `fontCss` / `customFonts` entries — pair it with the **Sketch** libraries
for a cohesive hand-drawn deck.

## What's inside

### Components (`pcf-components.xml`)

Capability, Platform, Sub-Capability, Capability Group, Capability Consumer,
Capability Owner, Service, External System, Data Store, Consumer API,
Producer API, Fleet, Desired vs Actual State, Outcome, Decision, Process Step,
Event, Start/End, Policy, Documentation, Note, Open Question, Reference,
Risk/Gap, Section/Layer, Swimlane, Tag, Title block, four edge styles
(provides / depends-on / exchanges / reconciles), and a set of plain
coloured rectangles.

### Icons (`pcf-icons.xml`)

| Group      | Icons                                                                                     |
| ---------- | ----------------------------------------------------------------------------------------- |
| `actors`   | ai-agent, bot, human, scheduled-job, team                                                 |
| `callouts` | danger, info, note, question, success, tip, warning                                       |
| `ops`      | bell, clock, cloud, code, cog, computer, dashboard, gear, key, lock, pipeline, shield, webhook |
| `status`   | degraded, deprecated, failed, healthy, pending                                            |

## Rebuilding the icon libraries

The icon `.xml` files are generated from the source SVGs in `icons/`. After
adding or editing an SVG, regenerate both clean and sketch libraries:

```bash
python3 scripts/build-icon-library.py
```

This bundles every SVG under `icons/<group>/` into `pcf-icons.xml` and
`pcf-icons-sketch.xml`. Conventions:

- Keep icons on a `48×48` `viewBox`.
- Use the PCF blue `#2E5C9E` as the primary fill — the build emits a yellow
  (`#B5915A`) colour variant automatically for any icon that uses it.
- Group SVGs into one of `actors`, `callouts`, `ops`, `status`.

## Repository layout

```
icons/                  Source SVGs (actors, callouts, ops, status)
scripts/                build-icon-library.py — bundles SVGs into libraries
pcf-components.xml       Component shape library (clean)
pcf-components-sketch.xml Component shape library (sketch)
pcf-icons.xml            Icon library (clean, generated)
pcf-icons-sketch.xml     Icon library (sketch, generated)
pcf-theme.json           Draw.io configuration: styles + libraries + fonts
test/                    Example diagram using the library
```
