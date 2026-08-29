# 41 — Bench Bill of Materials

### v1.0 — what to buy, in what order, to what spec

**Function:** Turn the test programs of docs 12 §4 (liquid, tests A–L) and docs
21–22 (solid, T1–T9 / M1–M4) into a procurement list a stranger can act on
without re-deriving the author's choices. The documents say *what each experiment
decides*; this says *what to put in the basket, in what quantity, and which
parameter of each item is acceptance-critical*. It adds no experiment, changes no
figure, and decides nothing — where it and a track document disagree, the track
document wins.

---

## 1. How to read this list — and what it deliberately omits

**No part numbers, no vendors, no prices.** Every entry is a *class plus the spec
that matters*. This is deliberate and it is not laziness:

- A SKU is the fastest-rotting thing in a record meant to be read decades from
  now — faster than a price, which doc 12 §4 already scopes as "2026
  order-of-magnitude, one currency, one region."
- Naming a vendor implies a validation that has not happened. Nothing here is
  built (doc 00 §9); no item on this list has been bought, wired, or run.
- What actually transfers is the **specification**: "±2% RH over 20–90%, with a
  calibration certificate" survives translation to any market and any decade.
  "Model X" does not.

Where a spec is genuinely load-bearing — the case where a cheaper part silently
invalidates the result — it is called out as **acceptance-critical**.

**Confidence grades** follow doc 00 §9. *Procurement-grade* means the item and
its spec are ordinary commerce and can be sourced today. *Sizing-grade* means the
**quantity** derives from a design figure that is itself graded, so it moves if
that figure moves. Nothing here is *measured*.

**The shared instrumentation spine is specified in doc 22 §7 and is not restated
here** — including the reason wet/dry-bulb psychrometry, not a capacitive sensor,
is required at the near-saturated and hot-regen nodes, and the channel-budget
warning. Buy that stack once; every test below reuses it. This document lists
only what each test adds on top.

### 1.1 What this list is not

**There is no system bill of materials, and there should not be one yet.** Plate
thickness, channel pitch, coated area and per-module fluid inventory are all
open — that is finding **F6**, gated on **M1** and **M3** — and the effective Δq
that sets sorbent inventory is **PENDING M2** (**F3**). A parts list for the
built system would therefore be a list of ungraded numbers wearing part numbers,
which is precisely what doc 00 §9 forbids. The bench program exists to close
those gates. This list buys the bench, not the machine.

---

## 2. Stage 1 — the cheap parallel set

Everything here runs concurrently and none of it gates anything else. Per doc 12
§4 and the README reconstruction path, this is where a reconstructor starts.

### 2.1 Test A — jar equilibrium *(the single highest-value $30 in the program)*

Decides the real a_w table that feeds every floor number and the X12 lift
inequality. Go/no-go: **40 wt% @ 33 °C ≤ 55% ERH**.

| Item | Spec that matters | Qty | Grade |
|---|---|---|---|
| Wide-mouth jars, sealing lid | PP or glass; lid must take a sensor pass-through without leaking; ~250–500 mL | 6–10 | procurement |
| Capacitive RH/T sensor | **Acceptance-critical: ±2% RH or better over 20–90% RH, with a calibration certificate.** SHT85/SHT45 class per doc 22 §7 | 1–2 | procurement |
| Calcium chloride | Food or technical grade, anhydrous or dihydrate; state which — the hydrate changes the mass you weigh out | ~1 kg | sizing |
| Lithium chloride | Comparison arm only; small quantity | ~50 g | sizing |
| Balance | 0.01 g resolution at ≥ 200 g capacity | 1 | procurement |
| Stable warm enclosure | Must hold **27 °C and 33 °C** setpoints; an incubator, proofing box or sous-vide bath — the same warm stack tests D/G/L reuse | 1 | procurement |
| Saturated-salt calibration standards | For checking the RH probe before trusting it: LiCl, MgCl₂, NaCl class | 1 set | procurement |

*Quantities are sizing-grade:* they assume ~100–200 mL of brine per concentration
across the 35/38/40/42/44 wt% ladder plus the LiCl arm, with enough spare to
remake a jar.

**The one place not to economise:** the RH probe. The go/no-go sits at 55% ERH and
the interesting band is 45–60%; a ±5% sensor cannot resolve a pass from a fail.

### 2.2 Test B — aerosol drift *(~$5, and it gates cabin connection)*

Decides whether a liquid contactor may ever touch breathing air (X3), and feeds
the doc 00 §8 safety register item 3.

| Item | Spec that matters | Qty | Grade |
|---|---|---|---|
| Bare mild-steel coupons | **Acceptance-critical: bare and unpainted** — the whole assay is that rust is visible. Any coating defeats it | 4–6 | procurement |
| Drift eliminator / demister media | The chain being tested, per doc 11 §3 | as designed | sizing |
| Small fan and duct section | Must reach the **maximum design face velocity**, not a comfortable one | 1 | sizing |
| Brine | Shares test A's CaCl₂ | — | — |

Run both **trickle and flooded**. The flooded case is the one that fails.

### 2.3 Test E — ERV core

Decides ε_lat, the fouling trend, and **CO₂ crossover < 5%** (X7, and the
interlock's credibility).

| Item | Spec that matters | Qty | Grade |
|---|---|---|---|
| Enthalpy-recovery core | Membrane type, stated ε; sized to the doc 00 §5 fresh-air flow | 1 | procurement |
| NDIR CO₂ sensors | **Acceptance-critical: two matched units** — crossover is a *difference* measurement, so an unmatched pair reports the offset, not the leak | 2 | procurement |
| U-tube manometer or differential pressure gauge | For the ΔP fouling trend | 1 | procurement |
| Salt-aerosol source | To drive the fouling trend at accelerated rate | 1 | sizing |

### 2.4 Tests J and J-K — CO₂ sorbents *(required-PENDING; gates X10/X11)*

The **breathing-air gate**: amine/ammonia slip for J, alkaline particulate/mist
carryover for J-K (doc 00 §8 item 4).

| Item | Spec that matters | Qty | Grade |
|---|---|---|---|
| Solid amine sorbent | Lewatit VP OC 1065 class | small lot | procurement |
| K₂CO₃ on apolar carbon | J-K only; **acceptance-critical: apolar carbon or TiO₂ support — alumina and MgO are prohibited** (X11), and an alumina control is part of the test | small lot | procurement |
| NDIR CO₂ sensor, ppm-resolving | Must resolve **1,000–1,500 ppm**, not just percent-level | 1 | procurement |
| Regeneration heat source | J: 85–95 °C. **J-K: 120/135/150 °C setpoints** — the higher band needs a different heater than the sous-vide stack | 1 | procurement |
| Slip assay | Amine/ammonia detection tubes or equivalent; alkaline carryover by wipe/filter | 1 set | procurement |

Run J-K only where a ≥ ~130 °C tap exists on the platform (X11).

### 2.5 Solid track T1 and T9 — feedstock and benchmark

| Item | Spec that matters | Qty | Grade |
|---|---|---|---|
| Aluminium hydroxide feedstock | **Acceptance-critical to F4: record whether it is freshly precipitated amorphous Al(OH)₃ or crystalline gibbsite.** A PXRD fail may be the feedstock, not the milling | per doc 21 §4 | sizing |
| Fumaric acid | Technical grade | per doc 21 §4 | sizing |
| Mortar and pestle | The mill-zero route (T1) | 1 | procurement |
| Commercial AlFu lot | Basolite A520 class, for the T9 benchmark arm | small lot | procurement |
| Outsourced PXRD + DVS | A service, not a purchase — book it before synthesising | per T4 | procurement |
| T8 silica-wheel benchmark quote | Also a solicitation, not a purchase: request it in parallel at zero cost — solid-track hardware waits on it as well as on M2 (doc 21 §2) | 1 quote | procurement |

---

## 3. Stage 2 — test I, the liquid gate

Nothing downstream on the liquid track is worth buying until test I reports.
Measure **irrigation rate first** — it is the variable doc 12 §4 names as the
first-order one, and CHK-019 records that the cell rating, face-velocity band and
NTU approach do not currently share an operating point.

| Item | Spec that matters | Qty | Grade |
|---|---|---|---|
| Film-cell structured packing | Per doc 11 §2; ~600 × 300 × 150 mm class | 1–2 cells | sizing |
| Wetted-path materials | **Acceptance-critical: the doc 11 §1 two-worlds law is absolute.** PP / PVC / PVDF / PE-RT / titanium only. No copper, brass, aluminium, zinc, 304 SS, and **no nylon** — CaCl₂ stress-cracks loaded polyamide | all | procurement |
| Wetted fasteners | PP / PVC / PVDF only. Plumbing-aisle parts hide brass | all | procurement |
| Distribution and pump | Must give a **controllable, measurable irrigation rate** — the primary variable | 1 | sizing |
| Rocking rig | 5–20° for the marine case; also the 30° passive-path rating (IN-016) | 1 | sizing |
| Flow measurement | Timed volumetric catch is sufficient (doc 22 §7) | — | — |

**Never** a brazed-plate exchanger anywhere brine or raw water flows: 304 plus
copper braze is a two-worlds violation (doc 11 §1).

---

## 4. Stage 3 and 4 — after the gates

Deliberately thin. Tests D, G and H, and the M1–M4 module set, reuse the warm
stack, the psychrometric stack and the fluid loop already bought above; doc 22 §5
specifies the single-coupon rig and doc 22 §7 the channels. The additions are:

| Test | Adds | Grade |
|---|---|---|
| D — regeneration COP | Still tray; **condenser with a measurable approach** | sizing |
| G — sealed-still rate | **TDS meter** — potability and entrainment both hinge on it (doc 00 §8 item 5) | procurement |
| H — M-cycle wetting | Wicking media; tilt fixture 5/10/15°; closed-loop feed path for the X8 point | sizing |
| M1–M4 | Second logger **or** the unified ESP32 + MAX31856/SHT node — see the doc 22 §7 channel-budget warning; gravimetric balance; oven with **independently thermocouple-verified** setpoints | procurement |
| F — endurance | Nothing. It is a locker and patience | — |

---

## 5. Reagent and consumable summary

| Consumable | Feeds | Indicative quantity | Grade |
|---|---|---|---|
| Calcium chloride | A, B, I, and the X12 arm | ~1 kg for A and B; **I is the step change** and its charge follows the cell design | sizing |
| Lithium chloride | A comparison arm | ~50 g | sizing |
| Fumaric acid + Al(OH)₃ | T1, T4 | per doc 21 §4 | sizing |
| Solid amine / K₂CO₃-on-carbon | J, J-K | small lots | procurement |
| Mild-steel coupons | B, and any materials re-check | 4–6 | procurement |
| Saturated-salt RH standards | Probe calibration before A | 1 set | procurement |
| Distilled water | The whole solid-track loop; M-cycle feed | ongoing | procurement |

---

## 6. Sequencing note

The order above is the README's cheapest-decisive-first path and it is not
arbitrary: **A** moves the largest single unknown for ~$30, **B** can veto the
entire liquid cabin-air architecture for ~$5, and **I** is the gate that decides
whether any liquid hardware is worth building. Buying stage 2 before stage 1
reports is how a program spends its budget on the wrong answer.

---
*Part of an open defensive-publication release: hardware CERN-OHL-P v2, text
CC-BY-4.0, scripts MIT. No patents sought or held. Unbuilt paper design — see
LICENSE for the safety disclaimer.*

*Version history*
- **v1.0** — New document. Consolidates the procurement layer of the doc 12 §4
  and doc 21–22 test programs into one ordered list, specified by class and
  acceptance-critical parameter rather than by part number. Records explicitly
  that no system bill of materials exists or should yet exist, because the
  geometry it would enumerate is open per F6/F3 and gated on M1/M2/M3. No
  experiment added, no figure changed.
