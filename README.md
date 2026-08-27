# Heat-Driven Comfort & Water — Land and Marine

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21544099.svg)](https://doi.org/10.5281/zenodo.21544099)

### Two desiccant tracks, one physics, one platform

**Sun or waste heat in — dry cool air, safe air quality, hot water, and drinking
water out**, for land and marine platforms in humid climates where the ambient dew
point sits above every ambient sink, so no evaporative or condensing device alone
can deliver comfort. Only a desiccant breaks that floor. This repository develops
**two complementary desiccant architectures** — a CaCl₂ brine system and an AlFu
MOF coated-exchanger system — plus the shared basis that connects them.

**Design point (sole): DP-A — 32 °C / 80% RH, ω 24.2 g/kg, dew point 28.1 °C,
raw-water sink ~29 °C** — the continuous-duty maximum for every mode. Milder
ambients are margin; excursions above DP-A are handled transiently, never by
sizing.

**Status:** paper designs. Liquid track gated by bench tests costing of order a few
hundred dollars (per-test estimates in doc 12 §4);
solid track by the T1/T2/M1–M4 program. Nothing built. Every quantitative claim
carries a confidence grade (doc 00 §9).

---

## Document lineage (v1.3 — this set supersedes all archived documents)

| File | Contents |
|---|---|
| **`00_platform_basis.md`** | **Read first.** Land+marine scope · DP-A · shared physics · the generalized airflow–moisture model · the CO₂ stack (<1,000 ppm spec) · exhaust-recovery doctrine (X8) · safety-critical requirements register |
| `10_liquid_concept_physics.md` | Liquid track: brine principle, mixed-mode baseline, moisture battery, berth-cascade M-cycle, performance envelope |
| `11_liquid_architecture_materials.md` | Two-worlds materials law, film-cell bank, aerosol control, sealed still + degradation ladder, ERV & CO₂-battery hardware, thermal bus, raw-water circuit, column annex, operating modes |
| `12_liquid_numbers_test_plan.md` | Validated quantities at DP-A, the errata trail, sensitivities, tests A–L with the dependency chart, rejected CO₂ alternatives |
| `20_solid_concept_system.md` | Solid track: architecture, the corrected F1 balance (~9–11 kg/h), regeneration-vs-purge physics (F2), X8 closed working loop, energy-source verdicts |
| `21_solid_sorbent_synthesis.md` | Isotherm-step selection, candidate table, aqueous + LAG routes, F4 branch, QC gates |
| `22_solid_module_validation.md` | DCHX design, coating rules, F5 chloride mitigations, bench rig, M1–M4, staged pipeline |
| `30_integration_energy_water.md` | Heat cascade, HDH, source roles, all-electric galley, water redundancy ladder, degraded operation |
| `31_upgrade_paths_sorption_cycles.md` | **Boost modes & upgrade paths (additions, never core):** the CaCl₂ absorption heat transformer (X12, primary — 60–65 °C tail → 85–90 °C at COP ~0.45–0.48), coupled VC heat pump, still MVR, closed AlFu chiller, static crystallizer pot; gates = tests L/A3 |
| `40_findings_register.md` | **Read before trusting any sizing figure.** F1–F6, X1–X12, X14, spec P17, tasks, make-or-break bench list |
| `parameter_register.xlsx` | **The quantitative register.** Every published figure with its unit, confidence grade, gating test, derivation and source section, plus live sheets that re-derive the headline numbers from the design point (doc 50 §3.5). Generated, not hand-edited |
| `diagrams/` | SVG set: mixed-mode air path · CO₂/ventilation trade-off · volume-threshold ladder · exhaust-recovery doctrine · CO₂ stack & battery |

Archived predecessors (superseded, retained for the record): the two original
track READMEs, `core-01..03`, `01..05`, and `06_cross_track_resolutions.md` —
whose patches P1–P20 are now applied in place throughout this lineage.

---

## The two tracks in one table (all at DP-A)

| | **Liquid track** (CaCl₂ brine, docs 10–12) | **Solid track** (AlFu DCHX, docs 20–22) |
|---|---|---|
| Role | **Solar-grade layer**: dehumidify to ~55% RH, berth-scale spot cooling, moisture + CO₂ batteries, degraded-mode backbone | **Waste-heat layer**: full AC (~17–18 °C supply, 3.5 kW sensible) + water surplus |
| Peak sorbent duty | 0.88 kg/h (100 m³ / 4 adults) | ~9–11 kg/h |
| Heat | ~0.92 kW peak · **~9–11 kWh/day with ERV** · 60–93 °C, any source incl. solar (sealed still — no purge wall, X2) | ~7.5–9 kW continuous · 60–65 °C but waste-heat-coupled at peak (F2) |
| Electricity | 25–80 W (+ ~2 kWh_e/day induction galley) | ~0.6–1.0 kW PENDING measured ΔP |
| Storage | Moisture battery ~35–40 kg/occupied night (25–55 kg spec) + CO₂ battery | Dry module as small thermochemical store |
| Water | 8–18+ L/day distillate; water-neutral berth M-cycle (X8 option) | **Water-neutral M-cycle in every ambient (X8)** + ~50–70 L/day potable surplus |
| CO₂ (<1,000 ppm spec) | Ventilation stack + TSA CO₂ battery (PENDING test J) | ~600 ppm open-cycle; X8 mode sizes ventilation for the spec |
| Cabin-air gates | Aerosol chain + test B; CO₂-bed slip + test J | Inert sorbent; F5 mitigations; test J if bed fitted |
| First decisive number | ~$30 (test A) | Mill-zero + outsourced PXRD/DVS |

They share the M-cycle stage, distilled-water loop, raw-water circuit, thermal
bus, instrumentation, the airflow–moisture model, and the X8/X9/P17 doctrines.
Whole-cabin AC on the liquid track converges to solid-track-class duty — the
tracks meet there, and the choice becomes a heat-source question.

## Headline findings (register: doc 40)

Once-through and whole-cabin M-cycle never compose (X1) · the sealed still
regenerates at solar grade where the solid bed cannot (X2) · mixed-mode
recirculation with a hard CO₂ interlock is the occupied baseline (X6) · ε ≥0.8
ERV latent recovery makes generous ventilation cheap (X7) · saturated exhausts
end in distillation recovery, closed working loop = water-neutral M-cycle (X8) ·
no combustion in the envelope (X9) · a two-bed solid-amine CO₂ battery holds
<1,000 ppm sealed for ~2 kWh/day of the same low-grade heat (X10,
required-PENDING test J).

## Reconstruction path (cheapest-decisive-first)

1. Read docs 00 → 10/20 → 40; accept the dew-point-floor argument and the DP-A
   basis.
2. Run tests **A** ($30), **B** ($5), **E** (~$80–150), **J** (~$150–300) in
   parallel, plus solid **T1** (mill-zero) and **T9** (commercial A520 lot).
3. Build the film cell; run test **I** (irrigation rate first) — the liquid gate.
4. Liquid bank build in mixed-mode with the interlock, ERV, and CO₂ bed → tests
   D/G → Phase-2 berth cascade (test H, shared with the solid track).
5. Solid-track hardware only after M2 delivers effective Δq and the T8 silica
   benchmark quote is in hand; run the doc 00 §4 model with your own loads before
   committing full T2 scope; provision X8 valving from the start.

## Licensing & disclosure

Open **defensive publication**: hardware **CERN-OHL-P v2**, documentation
**CC-BY-4.0**, scripts **MIT**. No patents sought or held; the dated public
record is intended as prior art. Unbuilt paper designs — no warranty. Safety:
the doc 00 §8 register is binding — CO₂ interlock (<1,000 target / 2,000 alarm /
per-room max sensing / mechanical minimum stop), no combustion appliances in the
envelope, aerosol and slip assays before any cabin connection, potability and TDS
tests before any water is drunk. Any build omitting these departs from this
design.

---

*Version history*
- **v1.0** — Lineage reset: clean document set (00/10–12/20–22/30/40) written
  from the latest revisions with all patches (P1–P20) applied in place; land +
  marine scope made explicit; DP-A sole; predecessors archived.
- **v1.1** — Doc 31 (upgrade paths: sorption cycles & heat pumps) added to the
  lineage; X12 recorded in doc 40 (v1.2); tests L and A3 registered in doc 12
  (v1.2) as platform-conditional entries outside the baseline gating budget.
- **v1.2** — `docs/parameter_register.xlsx` added: the cross-document
  quantitative register with live re-derivations of the headline numbers, plus
  its generator in `scripts/` (MIT); doc 50 (v1.1) records it as machine-readable
  enablement (§3.5) and makes release-time reconciliation of its `Checks` sheet a
  publication gate. Its first reconciliation pass produced basis-labelling
  clarifications across docs 00 (v1.2), 10 (v1.1), 12 (v1.3), 20 (v1.1) and 22
  (v1.1) — **no design figure changed** — plus two recorded open items in doc 40
  (v1.3): the coated-area denominator (gated on M1) and the ε_lat behind the ERV'd
  duty line (doc 12 §2 erratum 10, gated on test E).
- **v1.2.1** — Release-tooling and metadata pass; no design figure changed.
  `scripts/check_release.py` added: a mechanical gate for the structural half of the
  doc 50 §9 checklist (doc 50 → v1.2). The render pipeline now covers **every**
  document, repairing `executive_summary.pdf`, which had shipped un-rendered Mermaid
  source since v1.0; `render_docs.sh` gained a dependency preflight and npm versions
  are pinned so figure layout cannot drift between releases. Doc 30 → v1.2 (state-diagram
  labels aligned with their layout override, caught by the new gate) and the executive
  summary → v1.1 (provenance restated to docs 00–50). `CITATION.cff`, `.zenodo.json`,
  `LICENSE.md` and this file's lineage table brought back into sync.
- **v1.2.2** — Independent verification pass: 29 of 31 published figures re-derived
  from first principles reproduce within tolerance. Four findings recorded (doc 40
  v1.4, register `Checks` sheet) — the CO₂-battery duty basis (average vs
  at-all-times peak, the one with a safety-spec consequence), the X2 crossover
  temperature as a function of brine concentration, the cross-track latent-gains
  basis, and the contactor rating/velocity/approach triangle. The aggregate
  bench-cost headline is retired (doc 12 v1.4); per-test estimates stay, scoped as
  2026 order-of-magnitude figures. No design figure changed.
- **v1.3** — Genericisation and register pass. Doc 30 (v1.3) drops every
  prime-mover-specific reference in favour of the heat **grade** the comfort
  systems actually depend on, and states that dependence explicitly as a
  cascade-tap interface requirement (60–93 °C · 60–65 °C · ≥ ~130 °C); the peak
  temperature figure is removed as unused by any derivation in this lineage. Doc
  50 (v1.3) and `LICENSE.md` bound the no-patent declaration to this lineage's own
  subject matter — descriptive, **not a retraction**. Doc 40 (v1.5) records **F6**
  (the DCHX sensible-cycling bucket is unverified, magnitude OPEN) and **X14**
  (the thermal-swing sensible penalty is set by the inert-mass ratio, not by cycle
  time), with **X13 reserved** for a pending finding; docs 20 (v1.2) and 22 (v1.2)
  carry the matching PENDING marker, scope correction, and sizing qualifier. Doc
  22 (v1.2) also specifies the marine intake train by equipment class with its
  positive-pressure envelope condition, and doc 11 (v1.2) separates that
  intake-side duty from the outlet-side aerosol chain. Doc 00 (v1.3) records the
  dew-point IEC / M-cycle terminology equivalence, both forms retained. The
  parameter register was regenerated. **No design figure changed.** Versions
  v1.2, v1.2.1 and v1.2.2 were development increments that were never separately
  tagged or archived; their content is first deposited as part of this release,
  which is why the version history above carries entries the Zenodo version list
  does not.

---

> **Defensive publication notice.** This work is published as a deliberate
> public disclosure intended to constitute prior art under 35 U.S.C. § 102 and
> corresponding provisions worldwide. No patent protection is sought or held by
> the authors for any subject matter disclosed herein, and the authors intend
> this dated public record to preclude the patenting of the disclosed subject
> matter by any party. First published: 2026-07-25. Archived with DOI:
> [10.5281/zenodo.22134961](https://doi.org/10.5281/zenodo.22134961) (version DOI, 
> this exact record) · concept DOI 
> [10.5281/zenodo.21544099](https://doi.org/10.5281/zenodo.21544099) (all versions).

Licensing: hardware CERN-OHL-P v2 · documentation & diagrams CC-BY-4.0 ·
scripts MIT — see `LICENSE.md` for the scope map.
