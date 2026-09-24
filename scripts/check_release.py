#!/usr/bin/env python3
"""check_release.py — mechanical preflight for the doc 50 §9 publication checklist.

The checklist is prose, so nothing enforced it: that is how the executive
summary shipped its Mermaid blocks as raw code fences from v1.0 to v1.1, and how
CITATION.cff sat at v1.0 while the lineage moved to v1.2. This script turns the
structural half of the checklist into a gate that fails loudly.

    python3 scripts/check_release.py            # from the repo root
    python3 scripts/check_release.py --strict   # treat warnings as failures too

Exit status: 0 all checks pass · 1 one or more failures. Judgement items in the
§9 checklist (ORCID obtained, Wayback snapshots, Zenodo record published) are
outside its scope and stay manual. MIT, per the repository scope map.
"""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAIL, WARN, OK = [], [], []


def fail(msg): FAIL.append(msg)
def warn(msg): WARN.append(msg)
def ok(msg):   OK.append(msg)


def docs():
    return sorted(p for p in (ROOT / "docs").glob("*.md"))


# ---------------------------------------------------------------- structure --
def check_doc_structure():
    """Every doc carries an H1, a version subtitle, a version history, and the
    tri-license + no-patents footer (doc 00 §9, doc 50 §8)."""
    for d in docs():
        raw = d.read_text(encoding="utf-8")
        # Footer phrases wrap across lines in the source; compare on collapsed
        # whitespace so a line break is not mistaken for a missing statement.
        t = raw
        flat = re.sub(r"\s+", " ", raw)
        name = d.name
        if not re.search(r"^# \S", t, re.M):
            fail(f"{name}: no H1 title (render_docs.sh derives the PDF title from it)")
        if not re.search(r"^### v\d+\.\d+", t, re.M):
            fail(f"{name}: no '### vX.Y' version subtitle under the H1")
        if "*Version history*" not in flat:
            fail(f"{name}: no '*Version history*' block in the footer")
        if "No patents sought or held" not in flat:
            fail(f"{name}: missing the 'No patents sought or held' statement")
        if "CC-BY-4.0" not in flat or "CERN-OHL-P" not in flat:
            fail(f"{name}: footer does not restate the tri-license line")
    ok(f"document structure: {len(docs())} docs carry title, version, history and footer")


def check_version_history_matches_subtitle():
    """The subtitle version must appear as the newest bullet in the history."""
    for d in docs():
        t = d.read_text(encoding="utf-8")
        m = re.search(r"^### (v\d+\.\d+)", t, re.M)
        if not m:
            continue
        cur = m.group(1)
        if not re.search(rf"^- \*\*{re.escape(cur)}\*\*", t, re.M):
            fail(f"{d.name}: subtitle says {cur} but no '- **{cur}**' bullet in the version history")
    ok("version subtitles have matching version-history entries")


# ------------------------------------------------------------------ artifacts --
def check_rendered_set():
    """rendered/ must hold a PDF per doc, and none may be older than its source
    (doc 50 §3.3: the PDF set is the self-contained archival artifact)."""
    rendered = ROOT / "rendered"
    if not rendered.is_dir():
        fail("rendered/ does not exist")
        return
    stale = []
    for d in docs():
        pdf = rendered / (d.stem + ".pdf")
        if not pdf.exists():
            fail(f"rendered/{pdf.name} missing — every doc needs a PDF")
        elif pdf.stat().st_mtime < d.stat().st_mtime:
            stale.append(pdf.name)
    orphans = {p.stem for p in rendered.glob("*.pdf")} - {d.stem for d in docs()}
    for o in sorted(orphans):
        warn(f"rendered/{o}.pdf has no corresponding docs/{o}.md")
    if stale:
        fail("stale PDFs (older than their source) — re-run the render pipeline: "
             + ", ".join(stale))
    else:
        ok("rendered/ is complete and no PDF is older than its source")


def check_register():
    """The parameter register is regenerated with the PDF set (doc 50 §3.5/§8)."""
    reg = ROOT / "docs" / "parameter_register.xlsx"
    if not reg.exists():
        fail("docs/parameter_register.xlsx missing")
        return
    newer = [d.name for d in docs()
             if d.suffix == ".md" and d.stat().st_mtime > reg.stat().st_mtime]
    if newer:
        fail("parameter register is older than: " + ", ".join(newer)
             + " — re-run scripts/build_parameter_workbook.py")
    else:
        ok("parameter register is newer than every source document")


def check_no_mermaid_in_pdfs():
    """No PDF may contain raw Mermaid source — the v1.0–v1.1 executive-summary bug."""
    if not shutil.which("pdftotext"):
        warn("pdftotext not installed — skipped the raw-Mermaid check on rendered/")
        return
    bad = []
    for pdf in sorted((ROOT / "rendered").glob("*.pdf")):
        try:
            txt = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True,
                                 text=True, timeout=60).stdout
        except Exception as e:                      # noqa: BLE001 - report, never abort
            warn(f"could not read {pdf.name}: {e}")
            continue
        if re.search(r"^\s*(flowchart|stateDiagram|sequenceDiagram|graph)\s", txt, re.M):
            bad.append(pdf.name)
    if bad:
        fail("raw Mermaid source visible in: " + ", ".join(bad)
             + " — preprocess.py did not cover these documents")
    else:
        ok("no PDF contains raw Mermaid source")


def check_pdf_pagination():
    """Catch a silently broken render: a PDF collapsed onto one page, or one that
    lost its page-number footers.

    Both were produced on 2026-08-27 by a wkhtmltopdf built against unpatched Qt,
    which ignored --footer-* and failed to paginate — every document in the set
    became a single A4 page with the remaining content clipped off-canvas. The
    whole broken set passed every other check in this file, which is why this one
    exists. Page numbering now comes from style.css's @page @bottom-center box."""
    if not (shutil.which("pdftotext") and shutil.which("pdfinfo")):
        warn("poppler-utils not installed — skipped the PDF pagination check")
        return
    bad = []
    for pdf in sorted((ROOT / "rendered").glob("*.pdf")):
        try:
            info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                                  text=True, timeout=60).stdout
            txt = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True,
                                 text=True, timeout=60).stdout
        except Exception as e:                      # noqa: BLE001 - report, never abort
            warn(f"could not read {pdf.name}: {e}")
            continue
        m = re.search(r"^Pages:\s+(\d+)", info, re.M)
        if not m:
            bad.append(f"{pdf.name} (no readable page count)")
            continue
        pages = int(m.group(1))
        feet = len(re.findall(r"^\s*\d+/\d+\s*$", txt, re.M))
        if pages == 1 and len(txt) > 6000:
            bad.append(f"{pdf.name} (1 page holding {len(txt)} chars — collapsed render)")
        elif feet == 0 and pages > 1:
            bad.append(f"{pdf.name} ({pages} pages, no page-number footers)")
    if bad:
        fail("PDF pagination check failed: " + "; ".join(bad)
             + " — re-render with the pinned engine (doc 50 §3.3)")
    else:
        ok(f"all {len(list((ROOT / 'rendered').glob('*.pdf')))} PDFs paginate "
           "and carry page-number footers")


def check_docs_manifest():
    """The workbook generator pins a version per document in its DOCS list, and
    nothing compared it to the documents themselves.

    It drifted in v1.3 and again in v1.4 — caught both times only by remembering,
    which is not a control. A stale manifest ships a register whose cover sheet
    misstates which version of each document it was built from."""
    gen = ROOT / "scripts" / "build_parameter_workbook.py"
    if not gen.exists():
        warn("build_parameter_workbook.py missing — skipped the DOCS manifest check")
        return
    src = gen.read_text(encoding="utf-8")
    m = re.search(r"^DOCS = \[(.*?)^\]", src, re.S | re.M)
    if not m:
        warn("could not locate the DOCS list in build_parameter_workbook.py")
        return
    listed = dict(re.findall(r'\("([^"]+\.md)","(v[\d.]+)"', m.group(1)))
    bad = []
    for d in docs():
        sub = re.search(r"^### (v\d+\.\d+)", d.read_text(encoding="utf-8"), re.M)
        if not sub:
            continue
        if d.name not in listed:
            bad.append(f"{d.name} missing from DOCS")
        elif listed[d.name] != sub.group(1):
            bad.append(f"{d.name}: DOCS says {listed[d.name]}, document says {sub.group(1)}")
    for name in listed:
        if not (ROOT / "docs" / name).exists():
            bad.append(f"{name} in DOCS but not in docs/")
    if bad:
        fail("workbook DOCS manifest out of step: " + "; ".join(bad)
             + " — update DOCS in build_parameter_workbook.py and rebuild")
    else:
        ok(f"workbook DOCS manifest matches all {len(listed)} document versions")


def check_version_history_order():
    """Every *Version history* block must list ascending. Six documents had
    drifted out of order by v1.4 (two of them shipped that way in v1.3); the
    hand-fix held only until the next appended bullet, because nothing checked.
    The bullets are already machine-parseable — no frontmatter or new metadata
    convention is needed to enforce this."""
    for d in docs():
        txt = d.read_text(encoding="utf-8")
        if "*Version history*" not in txt:
            continue
        block = txt.split("*Version history*", 1)[1]
        vers = re.findall(r"^- \*\*v(\d+(?:\.\d+)*)\*\*", block, re.M)
        keys = [tuple(int(x) for x in v.split(".")) for v in vers]
        if keys != sorted(keys):
            fail(f"{d.name}: version history out of order: "
                 + " ".join("v" + v for v in vers))
    if not any("version history out of order" in f for f in FAIL):
        ok("every version history lists in ascending order")


def check_register_reproducible():
    """Layer 1: the committed register must be byte-identical to a fresh rebuild.

    check_register() above compares mtimes only, so a bare rebuild turned it
    green whether or not the content was right, and a hand-edit stayed invisible
    (doc 40 §3 recorded this after v1.3). The generator now emits deterministic
    bytes — pinned dcterms stamps, normalized zip entries — so this is an exact
    sha256 comparison: a mismatch means the committed file is hand-edited, stale,
    or built from a different generator. No timestamp false alarms are possible."""
    import hashlib, subprocess, tempfile
    gen = ROOT / "scripts" / "build_parameter_workbook.py"
    reg = ROOT / "docs" / "parameter_register.xlsx"
    if not (gen.exists() and reg.exists()):
        warn("generator or register missing — skipped the reproducibility check")
        return
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "rebuild.xlsx"
        r = subprocess.run([sys.executable, str(gen), str(tmp)],
                           capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            fail(f"generator failed during reproducibility rebuild: {r.stderr.strip()[:200]}")
            return
        h_new = hashlib.sha256(tmp.read_bytes()).hexdigest()
        h_old = hashlib.sha256(reg.read_bytes()).hexdigest()
        if h_new == h_old:
            ok("parameter register is byte-identical to a fresh rebuild (sha256)")
            return
        # diagnose: which members differ
        import zipfile
        try:
            za, zb = zipfile.ZipFile(reg), zipfile.ZipFile(tmp)
            names = sorted(set(za.namelist()) | set(zb.namelist()))
            bad = [n for n in names
                   if n not in za.namelist() or n not in zb.namelist()
                   or za.read(n) != zb.read(n)]
            detail = (", ".join(bad[:5]) + ("…" if len(bad) > 5 else "")
                      if bad else "container-level: trailing bytes or zip structure")
        except Exception:                           # noqa: BLE001
            detail = "unreadable"
        fail("parameter register differs from a fresh rebuild — hand-edited or "
             f"stale (differing members: {detail}). Regenerate with "
             "scripts/build_parameter_workbook.py; never edit the xlsx directly")


def _generator_list_ids(src, name):
    """First element of each tuple in a top-level `NAME = [...]` / `NAME += [...]`."""
    import ast
    ids = []
    for node in ast.parse(src).body:
        target = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = getattr(node.targets[0], "id", None)
        elif isinstance(node, ast.AugAssign):
            target = getattr(node.target, "id", None)
        if target != name or not isinstance(node.value, ast.List):
            continue
        for el in node.value.elts:
            if isinstance(el, ast.Tuple) and el.elts:
                first = el.elts[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    ids.append(first.value)
    return ids


def check_register_ids():
    """Layer 2: the generator's FINDINGS and TESTS must carry exactly the IDs the
    documents publish. IDs are structured tokens, so this is deterministic —
    unlike the numeric reconciliation, which stays a doc 50 §8/§9 human item.
    Catches 'F6/X14 recorded in doc 40 but missing from the register' and the
    reverse. Reserved gaps (X13) simply appear in neither set."""
    gen = ROOT / "scripts" / "build_parameter_workbook.py"
    if not gen.exists():
        warn("build_parameter_workbook.py missing — skipped the ID check")
        return
    src = gen.read_text(encoding="utf-8")

    d40 = (ROOT / "docs" / "40_findings_register.md").read_text(encoding="utf-8")
    doc_f = set(re.findall(r"^### (F\d+) — ", d40, re.M))
    doc_x = set(re.findall(r"^\| \*\*(X\d+)\*\* \|", d40, re.M))
    doc_findings = doc_f | doc_x | ({"P17"} if "Specification P17" in d40 else set())
    gen_findings = set(_generator_list_ids(src, "FINDINGS"))

    d12 = (ROOT / "docs" / "12_liquid_numbers_test_plan.md").read_text(encoding="utf-8")
    sec4 = d12.split("## 4.", 1)[1].split("\n## ", 1)[0]
    doc_tests = set(re.findall(r"^\| \*{0,2}([A-L](?:\d|-K)?)\b", sec4, re.M))
    gen_tests = {i for i in _generator_list_ids(src, "TESTS") if re.fullmatch(r"[A-L](\d|-K)?", i)}

    bad = []
    for label, doc, g in (("finding", doc_findings, gen_findings),
                          ("liquid test", doc_tests, gen_tests)):
        for i in sorted(doc - g):
            bad.append(f"{label} {i} in the documents but not the register")
        for i in sorted(g - doc):
            bad.append(f"{label} {i} in the register but not the documents")
    if bad:
        fail("register/document ID mismatch: " + "; ".join(bad)
             + " — update the generator lists and rebuild")
    else:
        ok(f"register IDs match the documents ({len(gen_findings)} findings, "
           f"{len(gen_tests)} liquid tests)")


def check_register_values():
    """Layer 3 (WARN-only): flag register rows whose numeric value does not
    appear in the text of their cited source section.

    Semantics are deliberately asymmetric. A non-match means INSPECT — the row
    may be restated in different units, a derived figure, or genuinely wrong; a
    human decides which (doc 50 §8). A match is weak evidence only, never
    verification — small integers match trivially. This check can therefore
    under-flag but cannot produce a false 'verified'. It feeds the doc 50 §9
    reconciliation pass; it does not replace it."""
    import ast
    gen = ROOT / "scripts" / "build_parameter_workbook.py"
    if not gen.exists():
        return
    src = gen.read_text(encoding="utf-8")
    rows = []
    for node in ast.parse(src).body:
        target = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = getattr(node.targets[0], "id", None)
        elif isinstance(node, ast.AugAssign):
            target = getattr(node.target, "id", None)
        if target == "REGISTER" and isinstance(node.value, ast.List):
            code = compile(ast.Expression(node.value), "<register>", "eval")
            rows += eval(code, {"N": None, "__builtins__": {}})   # noqa: S307 - literals + N only

    bynum = {}
    for d in docs():
        m = re.match(r"(\d\d)_", d.name)
        if m:
            bynum[m.group(1)] = d.read_text(encoding="utf-8")

    def section_text(docno, sec):
        txt = bynum.get(docno)
        if txt is None:
            return None
        base = sec.split(".")[0]
        m = re.search(rf"^## {base}\..*?(?=^## |\Z)", txt, re.M | re.S)
        return m.group(0) if m else txt

    flagged = []
    for row in rows:
        rid, vals, source = row[0], [v for v in row[5:8] if isinstance(v, (int, float))], row[12]
        if not vals:
            continue
        refs = re.findall(r"(\d\d) §([\d.]+)", source)
        if not refs:
            continue
        texts = [section_text(no, sec) for no, sec in refs]
        texts = [x.replace(",", "") for x in texts if x]
        if not texts:
            continue
        def present(v):
            s = f"{v:g}"
            return any(re.search(rf"(?<![\d.]){re.escape(s)}(?![\d])", x) for x in texts)
        missing = [v for v in vals if not present(v)]
        if missing:
            flagged.append(f"{rid} ({', '.join(f'{v:g}' for v in missing)} vs {source})")
    if flagged:
        warn(f"register values needing inspection — {len(flagged)} row(s) whose "
             "number was not found verbatim in the cited section (restatement, "
             "derived figure, or drift — human call per doc 50 §8): "
             + "; ".join(flagged[:8]) + ("; …" if len(flagged) > 8 else ""))
    else:
        ok("every numeric register value appears verbatim in its cited section")


# ------------------------------------------------------------------ metadata --
def _readme_latest_version(readme):
    vs = re.findall(r"^- \*\*(v\d+\.\d+(?:\.\d+)?)\*\*", readme, re.M)
    return vs[-1] if vs else None


def check_metadata_sync():
    """CITATION.cff, .zenodo.json and the README must agree on version and DOI
    (doc 50 §5; .zenodo.json takes precedence on the record itself)."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    zen = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))

    rv = _readme_latest_version(readme)
    cv = (re.search(r'^version:\s*"([^"]+)"', cff, re.M) or [None, None])[1]
    zv = zen.get("version")
    if rv and cv and zv and rv == cv == zv:
        ok(f"version is consistent across README, CITATION.cff and .zenodo.json ({rv})")
    else:
        fail(f"version mismatch — README {rv!r}, CITATION.cff {cv!r}, .zenodo.json {zv!r}")

    dois = set(re.findall(r"10\.5281/zenodo\.\d+", readme))
    cff_doi = re.search(r"10\.5281/zenodo\.\d+", cff)
    if not dois:
        fail("no Zenodo DOI found in README")
    elif cff_doi and cff_doi.group(0) not in dois:
        fail(f"CITATION.cff DOI {cff_doi.group(0)} does not appear in README")
    else:
        ok(f"DOIs consistent between README and CITATION.cff ({len(dois)} referenced)")

    if "Defensive publication notice" not in readme:
        fail("README is missing the verbatim defensive-publication notice (doc 50 §3.4)")
    else:
        ok("README carries the defensive-publication notice")


def check_license_layout():
    """Zenodo picks the alphabetically-first license file if several exist, so the
    root must carry LICENSE.md only and the texts must live in LICENSES/."""
    if (ROOT / "LICENSE").exists():
        fail("a root LICENSE file exists — it breaks Zenodo license detection (doc 50 §3.2)")
    if not (ROOT / "LICENSE.md").exists():
        fail("LICENSE.md scope map missing from the repository root")
    for t in ("CERN-OHL-P-2.0.txt", "CC-BY-4.0.txt", "MIT.txt"):
        if not (ROOT / "LICENSES" / t).exists():
            fail(f"LICENSES/{t} missing")
    if not FAIL:
        ok("license layout matches doc 50 §3.2")


# ------------------------------------------------------------------ diagrams --
def check_wide_overrides():
    """mmd_wide overrides may differ from the in-doc source in layout only: node
    and edge CONTENT must stay verbatim (scripts/mermaid-render/README.md)."""
    wide = ROOT / "scripts" / "mermaid-render" / "mmd_wide"
    if not wide.is_dir():
        warn("no mmd_wide/ directory — skipped the override check")
        return
    blocks = {}
    pat = re.compile(r"```mermaid\n(.*?)```", re.S)
    for d in docs():
        for i, m in enumerate(pat.findall(d.read_text(encoding="utf-8")), start=1):
            blocks[f"{d.stem}_{i:02d}"] = m

    def content(src):
        """Node/edge payload with the three sanctioned layout hints normalised away:
        an %%{init}%% spacing directive, invisible stacking edges (A ~~~ B), and a
        direction change (flowchart LR<->TD, or a stateDiagram `direction` line).
        Anything else that differs is a content change and must be reported."""
        keep = []
        for line in src.splitlines():
            ls = line.strip()
            if not ls or ls.startswith("%%"):
                continue
            if re.fullmatch(r"\S+\s*~~~\s*\S+", ls):
                continue
            if re.fullmatch(r"direction\s+(TB|TD|BT|LR|RL)", ls):
                continue
            ls = re.sub(r"^(flowchart|graph)\s+(TB|TD|BT|LR|RL)\b", r"\1", ls)
            keep.append(ls)
        return keep

    checked = 0
    for f in sorted(wide.glob("*.mmd")):
        key = f.stem
        if key not in blocks:
            fail(f"mmd_wide/{f.name} has no matching diagram in the doc set — stale override")
            continue
        if content(f.read_text(encoding="utf-8")) != content(blocks[key]):
            fail(f"mmd_wide/{f.name} differs from its in-doc source in node/edge content, "
                 "not layout alone")
        checked += 1
    if checked:
        ok(f"{checked} wide-diagram override(s) match their in-doc source verbatim")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = ap.parse_args()

    for fn in (check_doc_structure, check_version_history_matches_subtitle,
               check_rendered_set, check_register, check_no_mermaid_in_pdfs,
               check_pdf_pagination, check_docs_manifest, check_version_history_order,
               check_register_reproducible, check_register_ids, check_register_values,
               check_metadata_sync, check_license_layout, check_wide_overrides):
        try:
            fn()
        except Exception as e:                      # noqa: BLE001 - a broken check is a failure
            fail(f"{fn.__name__} raised {type(e).__name__}: {e}")

    for m in OK:   print(f"  ok    {m}")
    for m in WARN: print(f"  warn  {m}")
    for m in FAIL: print(f"  FAIL  {m}")
    print(f"\n{len(OK)} passed · {len(WARN)} warning(s) · {len(FAIL)} failure(s)")
    if FAIL or (args.strict and WARN):
        print("Release blocked. Judgement items in doc 50 §9 (ORCID, snapshots, "
              "Zenodo publish) remain manual.")
        return 1
    print("Structural checks pass. The doc 50 §9 judgement items remain manual.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
