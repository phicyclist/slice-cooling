# License scope map

This repository is a tri-licensed open defensive publication. Full verbatim
license texts live in `LICENSES/`; this file is the human map of which
license covers what.

| Scope | Contents | License |
|---|---|---|
| **Hardware designs & specifications** | System architectures, sizing, materials tables, synthesis routes, test rigs described in `docs/` | [CERN-OHL-P v2](LICENSES/CERN-OHL-P-2.0.txt) |
| **Documentation, data & diagrams** | All markdown documents, the executive summary, rendered PDFs, the parameter register (`docs/parameter_register.xlsx`), and the SVG set in `diagrams/` | [CC-BY-4.0](LICENSES/CC-BY-4.0.txt) |
| **Scripts & code** | Everything in `scripts/` (render pipeline, parameter-register generator, repo tooling) | [MIT](LICENSES/MIT.txt) |

The record-level license displayed by Zenodo is CC-BY-4.0 (documentation is the
bulk of the work), set explicitly in `.zenodo.json`; the tripartite scheme is
restated in the record description.

No patents are sought or held for any subject matter disclosed herein.

**Scope of that declaration.** It covers the desiccant comfort, water, and
air-quality subject matter developed in `docs/` — the scope of the CERN-OHL-P v2
and CC-BY-4.0 rows above. Upstream energy sources are referenced only generically
and only as interface requirements (a cascade tap at a stated grade, doc 30,
function statement); they are not subject matter disclosed here. This is
descriptive of intent and is **not a retraction** — nothing already published is
withdrawn by it (doc 50 §3.4).
