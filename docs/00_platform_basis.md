# 00 — Platform Basis: Scope, Design Point, Shared Physics & Doctrines

### v1.3 — foundation document for both tracks

**Function:** Everything both tracks share: deployment scope, the governing design
point, the shared psychrometric argument, the generalized airflow–moisture model,
the ventilation/CO₂ stack, the exhaust-vapor recovery doctrine, and the
safety-critical requirements register. Track documents (10–12 liquid, 20–22 solid,
30 integration) reference this document rather than restating it.

---

## 1. Scope — land and marine

The system targets **both land and marine deployment** in humid-tropical (and by
extension any humid) climates. Design rules are written to the *harshest common
case* so one document set covers both:

| Aspect | Marine (governing case) | Land relaxations |
|---|---|---|
| Raw-water sink | Seawater ~29 °C (tropical surface) | Lake/river/well water, often cooler (22–28 °C tropics; lower elsewhere) → every sorbent floor improves (see §3 leverage). No water sink: evaporative fluid cooler (approaches wet bulb ~30 °C — near parity) or dry cooler (approaches dry bulb 32 °C — floors rise ~1.5–2 g/kg; state the penalty) |
| Motion | Heel/roll to ~15–20°; flooded-mode fallbacks, staged headers, anti-slosh rules | Stationary: motion provisions optional, retained as shipped hardware margin |
| Salt aerosol at intake | Mandatory intake filtration / sealed paths | Coastal: keep; inland: may relax intake filtering only |
| Chloride materials rules | Full two-worlds discipline (doc 11 §1) | **Never relaxed** — the desiccant itself is the chloride source |
| Envelope | ~100 m³ occupied reference (yacht interior / small dwelling / cabin / shelter) | Same physics; volume thresholds per §6 ladder |

Terminology: "platform" = vessel or land site; "raw-water sink" = seawater or its
land equivalent. Marine values are used in all reference numbers; land is margin.

## 2. Governing design point (sole)

**DP-A: 32 °C / 80% RH · ω = 24.2 g/kg · dew point 28.1 °C · raw-water sink
~29 °C.** DP-A is the **continuous-duty maximum rating for every mode**. Milder
ambients are operating margin (every duty term shrinks monotonically with ambient
ω); rare excursions above DP-A are handled transiently — moisture-battery
draw-down, setpoint relaxation, boost — never by sizing. A prior secondary point
(30 °C / 75%) is retired; numbers derived from it in archived documents are
historical records.

Saturation humidity ratios used throughout (Magnus, 101.325 kPa): 26 °C → 21.3,
27 °C → 22.6, 28 °C → 24.1, 29 °C → 25.6, 30 °C → 27.1 g/kg.

**Air-density basis:** volumetric-to-mass air conversions throughout the lineage use
**ρ = 1.2 kg/m³** (standard air), not the ~1.15 kg/m³ of moist air at DP-A itself. Every
mass flow — and every duty derived from one — therefore runs ~5% high. The direction is
deliberate: it oversizes rather than undersizes. Stated here so it is an assumption on
the record rather than one implied by the arithmetic.

## 3. The shared physics — why a desiccant is non-negotiable

Comfort in humid heat requires removing water from air, and only two things do
that: a surface below the dew point (refrigeration) or a sorbent whose surface
vapor pressure sits below ambient (a desiccant). At DP-A every ambient sink — raw
water ~29 °C, outside air — sits **at or above the 28 °C dew point**, so:

- a sink-cooled condenser harvests ≈ zero water from ambient air;
- evaporative cooling (including the M-cycle) cannot go below the dew point —
  potent only once air is *pre-dried*;
- the desiccant breaks the floor because its surface vapor pressure is set by
  loading/concentration, not by a cold sink. The hard problem is **regeneration
  against near-saturated surroundings**, never capture.

**Terminology (equivalence).** The *dew-point indirect evaporative stage* —
short form *dew-point IEC* — is the cycle published as the **Maisotsenko cycle**
and written **M-cycle** throughout this lineage and in the HVAC literature. All
four terms denote the same stage. The generic forms are recorded so the
disclosure does not depend on an eponym or a trademark; the eponymous forms are
retained in the text so the record stays discoverable under the terms an
examiner or searcher will actually use.

Two sorbent families implement this: a CaCl₂ brine (liquid track, docs 10–12) and
an AlFu MOF coated exchanger (solid track, docs 20–22). Their regeneration physics
differ structurally — **finding X2**: the liquid track's sealed still has no purge
stream, so its driving force (hot-pool Pv vs ~4–5 kPa sink-cooled condenser) stays
positive at any pool temperature above ~40 °C and only *rate* degrades at low
grade; the solid bed desorbs into a condensing purge (~25 g/kg) and hits a
zero-driving-force wall below ~50 °C (F2). Consequence: **the liquid track is the
solar-grade layer; the solid track is the high-duty waste-heat layer.**

Raw-water leverage (both tracks): cooler sink water deepens every floor —
~0.5–0.7 g/kg per °C on the brine side; land installs with cool groundwater get
this for free.

## 4. The generalized airflow–moisture model

Closed steady-state balance replacing hand chains; the sorbent back-end enters
only through the supply humidity ω_sup (AlFu ~8 g/kg; brine per the doc 12 floor
matrix). Unknowns solved simultaneously:

1. ω_cab = ω_sup + latent_gains / S (cabin steady state)
2. T_sup = T_in − ε_dp · (T_in − T_dp(ω_work)) (M-cycle, ε_dp ≈ 0.7)
3. S = Q_sens / (c_p · (T_cab − T_sup))
4. Q_wet = S · c_p · (T_in − T_sup)
5. M = Q_wet / Δh_work, Δh_work = h_sat(T_exh) − h(working-air entry state)
6. Sorbent duty = (S − M)(ω_cab − ω_sup) + M(ω_amb − ω_sup)

Load-bearing outputs at DP-A: solid track full-AC duty **~9–11 kg/h** (doc 20 §5);
liquid mixed-mode duty **0.88 kg/h** (doc 12 §1); and **finding X1** — once-through
ventilation and whole-cabin M-cycle cooling never compose (drying 370–750 m³/h of
ambient supply costs 5.5–11 kg/h). A full transient model (task T2) supersedes
this steady state; it does not replace it.

## 5. Ventilation & CO₂ — the four-layer stack (X6/X7/X9/X10, spec P17)

**Specification (safety-critical): cabin CO₂ <1,000 ppm at all times, in every
mode including sealed; alarm + forced boost at 2,000 ppm.** Four occupants generate
~3.4 kg CO₂/day (**crew total**, not per person: 0.072 m³/h awake / 0.047 asleep); CO₂ leaves only with air
exchanged, so recirculation, cascades, and ERVs move moisture, never CO₂.

- **Layer 0 — eliminate (X9): all-electric galley, no gas or combustion appliances
  aboard/on-site.** One 2 kW burner emits ~0.26 m³/h CO₂ (3.6× the crew) plus
  ~0.25 kg/h combustion water; induction deletes both (~2 kWh_e/day).
- **Layer 1 — ventilate efficiently.** 48 m³/h CO₂-governed fresh-air floor
  (12 m³/h·person; also carries bioeffluents, odors, O₂). **ε_lat ≥ 0.8
  counterflow ERV** on the fresh/exhaust pair (CO₂ crossover <5%, test E);
  demand-controlled ventilation; **displacement ducting** — supply low to berths
  first, exhaust pickups high in every closable room (closed doors otherwise run
  +2,000–2,900 ppm over the main space); **per-room NDIR sensors, interlock keyed
  to the maximum reading**. Marginal cost of fresh air at DP-A: (1−ε_lat) ×
  10.4 g/kg ≈ 0.06 kWh_heat/day per m³/h at ε 0.8 (**ERV'd basis** — the bare-fresh
  equivalent is ~5× higher, and the two are quoted separately below).
- **Layer 2 — scrub the increment (X10): the CO₂ battery, required-PENDING
  test J.** Two-bed solid-amine thermal-swing sorbent (Lewatit VP OC 1065-class,
  or DIY PEI-on-silica) in the recirculation branch, post-dehumidification
  (45–55% RH is near-optimal for amine chemistry). Duty at the ventilation floor:
  ~1.6 kg/day; two ~3 kg beds on ~90-min half-cycles; ~91 m³/h at 50% single-pass
  capture rides the existing recirc flow (+50–150 Pa); **regeneration 85–95 °C off
  the same heat bus, ~1.0–1.3 kWh/kg → ~1.6–2.5 kWh/day**; CO₂-rich purge vented
  out (§7 rule 1). Loaded beds store the overnight obligation (~0.3 kg) →
  regeneration is solar-window schedulable. **Bed chemistry follows the heat
  grade (X11):** the scrubbing duty is chemistry-agnostic; select the sorbent
  by the highest heat grade reliably available, top down. **≥ ~130 °C tap
  (waste-heat platforms): K₂CO₃-on-apolar-carbon TSA** — same bed
  envelope (~4–5 kg/bed at ~0.5–0.65 mmol/g working), carbonation *wants* the
  45–55% RH placement (water is a reagent), regeneration 130–150 °C, food-grade
  chemistry with no amine-slip or oxidative-fade pathway (the breathing-air
  gate becomes an alkaline-carryover assay), required-PENDING test J-K;
  **alumina and MgO supports prohibited** (irreversible double-salt
  deactivation). **Solar grade only (60–95 °C): the amine resin above** —
  potash is equilibrium-dead below ~120 °C (an F2-analogue wall; the ETC's
  93 °C ceiling cannot regenerate it). Combinations run the ladder for
  redundancy: a platform fitting potash as primary retains a small amine bed
  (or accepts the open-mode fallback) for sealed operation through a heat
  outage. **This is the only path that holds
  <1,000 ppm sealed.** Fallback if test J fails: oversized ERV + DCV at
  120–190 m³/h → ~800–1,000 ppm, open conditions only, no sealed-mode guarantee.
  Rejected alternatives (quantified in doc 12 §5): zeolites (water outcompetes
  CO₂), seawater absorption (>6 m³/h equilibrated + re-humidifies the air),
  membranes at 0.1 kPa, algae (150+ kWh/day of light), liquid amines (slip into
  breathing air), chemical scrubbing (~15 kg/day soda lime — **emergency
  consumable only**).
- **Layer 3 — interlock.** CO₂-governed fresh damper with a **mechanical minimum
  stop** (no controller fault or economy setting can close ventilation below the
  floor); recirculation-only operation prohibited while occupied; scrubbing never
  substitutes for the ventilation floor.

**Control law:** optimize marginal ventilation against marginal scrubbing on heat
availability — heat-rich, open the damper toward ~600–800 ppm; heat-scarce or
sealed, the bed holds <1,000 at the floor.

CO₂ dose–response at the floor and below (4 occupants; why the interlock exists):
48 m³/h → 1,920 ppm awake; 36 → 2,420; 24 → 3,420; 12 → 6,420; sealed
(infiltration only) → ~7,600. Each 12 m³/h of fresh air cut saves ~3.8 kWh/day of
**bare-fresh** heat at DP-A (≈0.32 kWh/day per m³/h un-recovered; with the ε 0.8 ERV
fitted, the same cut saves only ~0.7 kWh/day) — a standing economic temptation the
interlock forecloses.

## 6. Volume-threshold ladder at DP-A (liquid track; solid track is full-AC class)

| Mode | Serviceable volume | Limit type |
|---|---|---|
| Once-through cascade M-cycle cooling | ~2–5 m³ per outlet (74–112 W) | dew point of working air |
| Unattended, 1 contactor, holding 13 g/kg | ~90 m³ (×2 per contactor) | contactor capacity vs 0.1 ACH |
| Unattended, 1 contactor, mold-safe (60–65% RH) | ~160–215 m³ | " |
| Once-through occupied (pressure integrity) | ~110–240 m³ | supply ≥ 2–3× infiltration |
| **Mixed-mode occupied (baseline)** | **~300–500 m³** with a 3-cell bank | bank capacity + heat budget |
| Whole-cabin AC (recirc + hot-regen brine) | 100 m³-class at ~10.6 kg/h, ~11 kW heat | deferred — converges with the solid track |

Diagram: `diagrams/dpa-volume-thresholds.svg`.

## 7. Exhaust-vapor recovery doctrine (X8)

All *deliberately saturated* process exhausts terminate in distillation recovery
when marginal regeneration heat is available; heat is recaptured where practical.
Diagram: `diagrams/exhaust-recovery-doctrine.svg`.

1. **No double duty.** A stream is a rejection sink *or* a recovery source, never
   both — recapturing deliberately exported moisture re-imports the load just paid
   to reject.
2. **ERV protection.** The ducted room exhaust is reserved as the ERV moisture
   sink; the ERV outlet leaves near-saturated *by design* and is discharged
   un-recaptured.
3. **Saturated process exhausts end in recovery:** the M-cycle working stream
   closes on the desiccant loop (solid track: design intent, doc 20 §8; liquid
   track: valved free-heat option at ~1.3 kWh/L, doc 10 §6); the air-swept
   regeneration exhaust (degraded mode) gains a raw-water condenser — its
   condensate is **technical-grade only, PENDING TDS assay** (entrainment).
4. **Heat-recapture order:** DHW tank first (demand-capped ~1–3 kWh/day) →
   bed-to-bed / brine-to-brine recuperation → raw-water sink last. Adsorption heat
   releases only a few kelvin above the sink — reject it, don't chase it.

## 8. Safety-critical requirements register

Any build omitting these departs from this design:

1. CO₂ interlock per §5: <1,000 ppm target, 2,000 alarm/boost, per-room max
   sensing, mechanical minimum stop on the fresh damper.
2. No gas or combustion appliances in the conditioned envelope (X9).
3. Aerosol control chain + steel-coupon acceptance (test B) before any liquid
   contactor connects to breathing air (doc 11 §3).
4. CO₂-sorbent breathing-air assay before any bed connects to breathing air:
   amine/ammonia slip (test J) for amine beds; alkaline particulate/mist
   carryover (test J-K) for carbonate beds.
5. Distillate potability: independent water-quality test before regular
   consumption; air-swept-condenser water never enters potable or M-cycle-feed
   service before a TDS assay clears it.
6. Crystallization interlock: 42 wt% high-SG cutoff unless brine ≥22 °C
   guaranteed; 43 wt% storage cap (doc 11 §4).
7. Two-worlds materials rule on every brine/raw-water-wetted component (doc 11 §1).

## 9. Conventions

Confidence grades on every quantitative claim: **measured** · **procurement-grade**
· **sizing-grade** · **PENDING <test/task>**. DP-A on every number. Diagrams:
Mermaid inside documents; the SVG architecture set lives in `diagrams/`.
Psychrometric chains as state tables. Surgical edits with version bumps.

---
*Part of an open defensive-publication release: hardware CERN-OHL-P v2, text
CC-BY-4.0, scripts MIT. No patents sought or held. Unbuilt paper design — see
LICENSE for the safety disclaimer.*

*Version history*
- **v1.0** — New lineage. Consolidates the shared basis from the archived core-01
  §1, 01 §1–2, and 06 §§1–3, 9–11; land+marine scope made explicit; DP-A sole;
  CO₂ stack (P17, X9/X10), X8 doctrine, and safety register carried in place.
- **v1.1** — X11: heat-grade-dependent CO₂-bed ladder added to §5 Layer 2
  (K₂CO₃/apolar-carbon TSA for ≥ ~130 °C taps, test J-K; alumina/MgO support
  prohibition; amine bed retained at solar grade and as outage fallback);
  safety-register item 4 generalized to cover the carbonate alkaline-carryover
  assay.
- **v1.2** — Clarifying pass from the parameter register (doc 50 §3.5), no design
  figure changed: the ρ = 1.2 kg/m³ air-density basis stated explicitly in §2; the
  CO₂ generation rate in §5 labelled *crew total* to foreclose a 4× misreading;
  the §5 marginal-ventilation costs labelled ERV'd vs bare-fresh, which are on
  different bases and were previously quoted side by side without distinction.
- **v1.3** — Terminology equivalence note added (§3): *dew-point indirect
  evaporative stage* / *dew-point IEC* recorded as equivalent to the *Maisotsenko
  cycle* / *M-cycle*, both forms retained so the disclosure depends on neither an
  eponym nor a trademark. Prime-mover reference in the X11 heat-grade ladder (§5)
  genericised to waste-heat platforms. No figure changed.
