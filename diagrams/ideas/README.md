# Diagram ideas from the paragraph-by-paragraph compression

Candidate figures for the concepts the compression pass marked `→ DIAGRAM` and
ranked in its "highest-value gaps" table. They are sketches for discussion, not
part of the paper set in `diagrams/`; the three "already working" figures
(friction loop, architecture lineage, roles triangle) stay there.

Same toolchain as the paper set: edit the `.spec.json`, then

```bash
python3 scripts/build-diagram.py diagrams/ideas/<name>.spec.json
python3 scripts/restyle-diagram.py diagrams/ideas/<name>.drawio
python3 scripts/render.py diagrams/ideas/<name>.drawio --pdf-check
python3 scripts/combine-diagrams.py --output diagrams/ideas/pcf-diagram-ideas.drawio diagrams/ideas/[0-9]*.drawio
```

Open `pcf-diagram-ideas.drawio` for all sixteen as tabs.

| Tab | Paper location | The one idea it must land |
| --- | --- | --- |
| 01 volume vs variety | Part 1 ¶3 | Hiring moves the volume axis only; variety brings its own experts |
| 02 three-condition check | Part 1 ¶8 | The trigger is three conditions, not headcount |
| 03 builder to guarantor | Part 2 ¶1 | The platform team's job changes from building to guaranteeing |
| 04 contract vs API | Part 3 note | Two interfaces, two audiences: contract (platform, producer), API (capability, consumer) |
| 05 marketplace beside the flow | Part 3 ¶2 | Pair for `challenge-central-bottleneck`: platform team beside the flow, not in it |
| 06 factor admission test | Part 4 framing | Two gates: avoidable cost imposed, and not implied by another factor |
| 07 opinionation spectrum | Part 1 ¶10 | Flexibility vs usability; an un-opinionated platform is a raw cloud console |
| 08 capability anatomy | Part 2 ¶6 | Outcome, defined API, managed lifecycle, participation contract |
| 09 factors four plus foundation | Factor 5 ¶6 | Operational Evidence is what makes the other four verifiable |
| 10 declarative vs reconciliation 2x2 | Factor 4 ¶2 | Request shape and re-apply behaviour are independent axes |
| 11 dependency vs prerequisite | Factor 3 ¶2 | The ownership boundary; whoever creates a resource holds its lifecycle |
| 12 cost displacement | Part 5 ¶1 | Complexity does not vanish, it relocates; the factors decide where |
| 13 control vs data path | Factor 1 ¶4 | Request the database through the platform, talk to it directly |
| 14 declarative vs imperative | Factor 2 ¶2 | The ownership line moves when the consumer must know the steps |
| 15 one instance vs the fleet | Factor 4 ¶5 | The same declared state applied safely across many instances |
| 16 actors and their questions | Factor 5 ¶3 | Every actor answers its own question, without the producer |

Not built: the two-sided handshake (covered by `participation-contract`), the
documentation vs telemetry columns (covered by `factor-5-operational-evidence`),
the abstraction boundary and progressive-disclosure sketches (Part 2 ¶7,
Factor 3 ¶4), which need a non-grid composition.
