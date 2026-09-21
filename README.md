# Platform Capabilities Framework — Draw.io Library

A Draw.io / diagrams.net shape library for diagramming platform capabilities,
services, ownership, and operational state. It ships a consistent visual
language (the **PCF** palette and a hand-drawn **Comic Sans MS** sketch font) so
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

The **Sketch** libraries use **Comic Sans MS** — a system font, so nothing is
downloaded — for a cohesive hand-drawn deck.

## Diagrams in this repo

The [`diagrams/`](diagrams/) folder holds example diagrams built from the PCF
components. Draw.io stores each shape's full style *inline*, so these files
always **render with the PCF look** — open them anywhere, no setup required.

What a `.drawio` file *can't* record is which shape libraries are open in the
editor (that's app state, not file state). So to edit a diagram with the PCF
palettes docked in the left panel, use one of the two routes below.

### Open in the browser (zero install)

These links open the diagram in diagrams.net **with all four PCF libraries
pre-loaded** via the `clibs` URL parameter:

<!-- regenerate with: python3 scripts/make-open-links.py -->

| Diagram | Open in diagrams.net (libraries pre-loaded) |
| ------- | -------------------------------------------- |
| `centralized-friction-loop-landscape.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fcentralized-friction-loop-landscape.drawio) |
| `centralized-friction-loop.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fcentralized-friction-loop.drawio) |
| `challenge-central-bottleneck.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fchallenge-central-bottleneck.drawio) |
| `ecosystem-architecture-lineage-landscape.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fecosystem-architecture-lineage-landscape.drawio) |
| `ecosystem-architecture-lineage.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fecosystem-architecture-lineage.drawio) |
| `ecosystem-value-exchange.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fecosystem-value-exchange.drawio) |
| `factor-1-defined-contract-landscape.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Ffactor-1-defined-contract-landscape.drawio) |
| `factor-1-defined-contract.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Ffactor-1-defined-contract.drawio) |
| `factor-2-declarative-inputs.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Ffactor-2-declarative-inputs.drawio) |
| `factor-3-encapsulated-dependencies.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Ffactor-3-encapsulated-dependencies.drawio) |
| `factor-4-stable-reconciliation.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Ffactor-4-stable-reconciliation.drawio) |
| `factor-5-operational-evidence.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Ffactor-5-operational-evidence.drawio) |
| `factors-overview.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Ffactors-overview.drawio) |
| `factors-to-outcomes.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Ffactors-to-outcomes.drawio) |
| `participation-contract-landscape.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fparticipation-contract-landscape.drawio) |
| `participation-contract.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fparticipation-contract.drawio) |
| `pcf-community-draft.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fpcf-community-draft.drawio) |
| `platform-with-capabilities-landscape.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fplatform-with-capabilities-landscape.drawio) |
| `platform-with-capabilities.drawio` | [Open](https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-components-sketch.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fpcf-icons-sketch.xml#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FmissBerg%2Fplatform-capabilities%2Fmain%2Fdiagrams%2Fplatform-with-capabilities.drawio) |
