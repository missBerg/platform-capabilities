# platform-capabilities — agent guide

A draw.io / diagrams.net shape library (the **PCF** visual language) plus tooling
to author on-brand diagrams from a spec.

## Making a diagram (use the `pcf-diagram` skill)

The reliable loop — never skip the render step:

1. Write `diagrams/<name>.spec.json` (schema in `.claude/skills/pcf-diagram/SKILL.md`).
2. `python3 scripts/build-diagram.py diagrams/<name>.spec.json` → `<name>.drawio`.
3. `python3 scripts/render.py diagrams/<name>.drawio` → `<name>.png`; **read the
   PNG and fix overlaps/routing**, then regenerate until it looks clean.

The generator parses `pcf-components.xml` / `pcf-icons.xml` as the single source
of truth, so generated diagrams are always on-brand. `.drawio` files carry PCF
styles inline and render anywhere with no library install.

## Scripts (stdlib Python only — no third-party deps)

- `scripts/build-diagram.py` — spec → `.drawio`; `--self-check` validates libraries.
- `scripts/render.py` — `.drawio` → PNG/SVG via the draw.io desktop CLI
  (`brew install --cask drawio`; binary auto-located, or set `DRAWIO_BIN`).
- `scripts/build-icon-library.py` — rebuild icon libs after editing `icons/*.svg`.
- `scripts/make-open-links.py` — regenerate the README's diagrams.net deep links.

## Conventions

- Commits are DCO-signed (`git commit -s`) with Conventional Commit subjects.
- Branch before a PR; never commit on `main` directly. Use `gh` for GitHub.
- Keep icons on a 48×48 viewBox; primary fill PCF blue `#2E5C9E` (a yellow
  `#B5915A` variant is auto-generated). Regroup under `actors/callouts/ops/status`.
- Sketch flavour uses **Comic Sans MS** (a system font); the library shapes and
  the generator carry it inline.
