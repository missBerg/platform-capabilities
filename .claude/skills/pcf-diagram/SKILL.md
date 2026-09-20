---
name: pcf-diagram
description: Create a good-looking PCF (Platform Capabilities Framework) draw.io diagram from this repo's shape library. Use whenever someone wants a new .drawio diagram, an architecture/capability/flow picture, or to edit an existing PCF diagram in this repo. Produces on-brand diagrams via a JSON spec → generator → render-and-verify loop.
---

# Authoring PCF draw.io diagrams

This repo is a draw.io shape library (`pcf-components.xml`, `pcf-icons.xml`) plus
a generator that turns a small JSON spec into an on-brand `.drawio` file. Styling
is automatic because the generator **parses the library as the source of truth**;
your job is to get the *content and layout* right.

## The workflow — always do all three steps

1. **Write a spec** `diagrams/<name>.spec.json` (schema below).
2. **Generate**: `python3 scripts/build-diagram.py diagrams/<name>.spec.json`
   → writes `diagrams/<name>.drawio`.
3. **Render and LOOK**: `python3 scripts/render.py diagrams/<name>.drawio`
   → writes `diagrams/<name>.png`. **Read the PNG back** and check for overlaps,
   cut-off labels, edges crossing nodes, or tangled routing. Fix the spec and
   repeat until it looks clean. Do not skip this — it is the main quality lever.

Validate the libraries any time with `python3 scripts/build-diagram.py --self-check`.

## Spec schema

```jsonc
{
  "name": "Fig 1 – Bottleneck",   // optional; draw.io tab name (defaults to the file stem)
  "title": "My Diagram",          // optional; drawn top-left
  "flavour": "clean",             // "clean" (Helvetica) | "sketch" (hand-drawn)
  "direction": "LR",              // "LR" lanes=columns | "TB" lanes=rows
  "lanes": ["Producers","Core","Consumers"],   // optional; sets lane order
  "nodes": [
    {"id":"a","type":"capability","label":"Billing","sublabel":"charge customers",
     "lane":"Core","icon":"shield","iconColor":"blue","section":"Platform"},
    {"id":"u","type":"icon","icon":"human","label":"User","lane":"Producers"}
  ],
  "edges": [
    {"source":"u","target":"a","type":"provides","label":"uses"}
  ]
}
```

- **node**: `id` (unique; must NOT end in `-<number>` or `-icon`), `type` (slug
  below; default `rectangle-blue-light`), `label`, `sublabel` (2nd grey line),
  `lane`, `icon` (adds a corner badge), `iconColor` (`blue`|`yellow`),
  `section` (string — nodes sharing it get wrapped in a container),
  `sectionType` (container slug, default `capability-group`), `w`/`h` overrides.
- **icon node**: `type:"icon"` + `icon:"<slug>"` → a bordered icon tile.
- **edge**: `source`, `target`, `type` (`provides`|`depends`|`exchanges`|
  `reconciles`), optional `label`. Edges auto-route (orthogonal) — no coordinates.

## Component type slugs

Core: `capability` `platform` `sub-capability` `service` `external-system`
`data-store` `outcome` `decision` `process-step` `event` `policy`
`capability-consumer` `capability-owner` `consumer-api` `producer-api` `fleet`
`desired-vs-actual-state` `start-end`
Docs/meta: `documentation` `note` `open-question` `reference` `risk-gap`
Containers (use as `section`/`sectionType`): `capability-group` (dashed),
`section-layer` (titled swimlane), `swimlane-vertical`
Misc: `tag` `tag-blue` `title-block`
Plain fills: `rectangle-{blue,yellow,grey}-{light,dark}`

## Icon slugs (`icon:` field)

- actors: `human` `team` `bot` `ai-agent` `scheduled-job`
- callouts: `info` `tip` `note` `question` `success` `warning` `danger`
- ops: `cog` `gear` `key` `lock` `shield` `bell` `clock` `cloud` `code`
  `computer` `dashboard` `pipeline` `webhook`
- status: `healthy` `degraded` `failed` `pending` `deprecated`

Most icons also have a yellow variant — set `"iconColor":"yellow"`.

## Color semantics (keep diagrams legible)

- **Blue** = primary domain (capabilities, platform, services, consumers).
- **Gold/tan** = decisions, producers, ownership, policy.
- **Red** = risks, gaps, open questions.
- **Grey** = neutral, external, infrastructure.

Pick `type` slugs whose built-in color matches the meaning; don't fight it.

## Layout tips

- Put each logical column/row in its own `lane`; the generator grids within
  lanes and never overlaps nodes.
- Group related nodes with `section` to get a labelled container behind them.
- Keep cross-lane edges few; left→right (`LR`) for producer→capability→consumer,
  top→down (`TB`) for process flows.

## Known limitations (finish by hand when needed)

The generator gets ~90% there. Dense edge routing can still clip a node, and
two-label shapes (`start-end`, `desired-vs-actual-state`) only set the first
label. For final polish, open the `.drawio` in draw.io / VS Code and nudge
waypoints — that file already carries PCF styles inline, so it stays on-brand.
The sketch flavour uses **Comic Sans MS** — a system font the library shapes
carry inline, so no web font is downloaded.

## Layout and label knobs (spec fields)

- `laneGap` / `rowGap` (top level) — gap between lanes and between nodes
  within a lane, in px. Defaults 90 / 40.
- `{"type":"spacer","w":..,"h":..}` node — invisible, occupies grid space.
  In `TB` layouts a leading spacer centres a narrower row under a wider one
  (spacer w = (wideRow − thisRow) / 2 − laneGap); a whole spacer lane adds
  vertical room, e.g. so a section header does not collide with the row above.
- Edge `exit` / `entry` (`left|right|top|bottom`) pin the connection sides.
  Person stamps (`capability-owner`, `capability-consumer`) only connect
  cleanly on left/right; in `TB` flows use `rectangle-*-light` + a `team` /
  `human` icon badge instead.
- Edge `labelPosition` (−1 source … 0 middle … 1 target) slides the label
  along the edge.
- Edge `labelOffset` (px, vertical) and `labelOffsetX` (px, horizontal) push
  the label off the line. These are **page axes, not edge axes**: use
  `labelOffset` on horizontal edges and `labelOffsetX` on vertical ones.
- Edge `"route":"straight"` skips the orthogonal router.

## Paper figures (PDF budget)

Figures embedded in a document scale to the text column, so keep the canvas
narrow rather than wide: prefer `TB` (portrait) layouts, canvas width ≤ 550
units, labels 14 px, sublabels/edge labels 12 px. Run
`python3 scripts/render.py X.drawio --pdf-check` to see the effective point
size. No titles inside the image (the document caption carries it), sublabels
≤ 4 words, no red "fails the factor" callouts (the document states the cost
of failing; the figure shows the key point), and run
`scripts/restyle-diagram.py` after generating.
