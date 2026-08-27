# Mermaid render sub-pipeline (MIT)

Renders Mermaid blocks in lineage docs to PNG for the archival PDF set (doc 50 §3.3).

Dependencies (no system Chrome needed — Chromium ships inside the npm tarball):

    npm install          # exact versions pinned in package.json

Versions are pinned rather than ranged on purpose: the rendered PDF set is the
archival artifact (doc 50 §3.3), and a floating renderer changes figure layout
between releases for no recorded reason.

Flow (driven by ../render_docs.sh):
1. `preprocess.py <src> <mmd_dir> <md_out>` — extracts each ```mermaid block to
   `<doc>_<nn>.mmd`, substitutes an image reference in the copied markdown.
   Processes **every** `*.md` in the source directory; `render_docs.sh` uses the
   same glob and the two must stay in agreement. A numbered-only glob shipped
   `executive_summary.pdf` with raw Mermaid code fences from v1.0 to v1.1.
2. `mmrender.mjs <mmd_dir> <png_dir>` — renders each .mmd at 2× device scale,
   theme "neutral", `useMaxWidth:false` (natural size).
3. Wide diagrams (>~1600 CSS px natural width) — reflow first, rotate last:
   drop an adjusted copy in `mmd_wide/` (rendered over the canonical PNG name),
   using, in order of preference:
     a. direction swap — `flowchart LR` ↔ `TD` (siblings stack perpendicular
        to flow, so the overlong axis usually flips); stateDiagram-v2 takes a
        `direction LR` line;
     b. invisible edges (`A ~~~ B`) between nodes of side-by-side subgraphs to
        stack the subgraphs vertically;
     c. an init directive to tighten layout:
        %%{init: {"flowchart": {"nodeSpacing": 25, "rankSpacing": 35}}}%%
   Only if no reflow fits does `imgfix.py` rotate the figure 90° automatically
   and place it on its own page.
4. `imgfix.py <html>` — sizes, rotates, and page-isolates figures in the pandoc
   HTML before wkhtmltopdf.

Current mmd_wide/ overrides (v1.0 set): 10_liquid (LR→TD), 11_02 state diagram
(direction LR), 30_02 (LR + tightened spacing), 40_01 (invisible stacking edges
+ tightened spacing). Node/edge content is verbatim in every override — layout
hints only.

The verbatim rule on `mmd_wide/` is enforced by `../check_release.py`, which
compares each override against its in-doc source with the three sanctioned layout
hints (init directive, invisible edges, direction change) normalised away, and
fails on any other difference.

If mermaid-cli (`mmdc`) with a working Chrome is available locally, it can
replace steps 2–3; keep output filenames identical.
