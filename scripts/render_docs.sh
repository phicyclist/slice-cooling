#!/usr/bin/env bash
# render_docs.sh v3 — lineage docs → PDF with rendered Mermaid diagrams
# Pipeline: preprocess.py (mermaid → PNG refs) → mmrender.mjs (Chromium via
# @sparticuz/chromium + mermaid.js → 2x PNG) → pandoc → imgfix.py → WeasyPrint.
# Ultra-wide diagrams (>1600 CSS px) are rotated 90° as full-height figures. MIT.
#
# Renders EVERY .md in the source directory. Do not narrow this to the numbered
# docs: executive_summary.md carries diagrams too, and a numbered-only glob
# silently shipped its Mermaid blocks as raw code fences from v1.0 to v1.1.
# Keep this glob and preprocess.py's in agreement.
set -euo pipefail
shopt -s nullglob

SRC="${1:-md_pre}"; OUT="${2:-out}"; CSS="style.css"

# Preflight: fail loudly and early rather than half-way through the set.
missing=()
for tool in pandoc weasyprint python3; do
  command -v "$tool" >/dev/null 2>&1 || missing+=("$tool")
done
[ -f "$CSS" ]      || missing+=("$CSS (copy from scripts/)")
[ -f imgfix.py ]   || missing+=("imgfix.py (copy from scripts/mermaid-render/)")
if [ ${#missing[@]} -gt 0 ]; then
  printf 'render_docs: missing prerequisite(s):\n'; printf '  - %s\n' "${missing[@]}"
  printf 'The pipeline is flat-cwd — run it from a staging directory, not the repo root.\n'
  exit 1
fi
python3 -c 'import PIL' 2>/dev/null || { echo "render_docs: imgfix.py needs pillow (pip install pillow)"; exit 1; }

# The rendered set is the archival artifact (doc 50 §3.3), so the PDF engine is
# pinned exactly like the npm renderer in package.json. This assertion exists
# because the previous engine, wkhtmltopdf, silently produced a collapsed
# single-page set with no page-number footers when built against unpatched Qt —
# and every structural release check passed it.
WEASY_PIN="69.0"
weasy_have="$(weasyprint --version 2>&1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1)"
if [ "$weasy_have" != "$WEASY_PIN" ]; then
  echo "render_docs: weasyprint '$weasy_have' found, pinned at $WEASY_PIN."
  echo "  Layout is version-sensitive. Install the pin (see"
  echo "  scripts/mermaid-render/requirements.txt), or bump WEASY_PIN"
  echo "  deliberately and re-verify the whole set by eye."
  exit 1
fi

docs=("$SRC"/*.md)   # nullglob: empty array when nothing matches; bash sorts the expansion
if [ ${#docs[@]} -eq 0 ]; then
  echo "render_docs: no .md files in '$SRC' — did preprocess.py run?"; exit 1
fi

mkdir -p "$OUT"
count=0
for md in "${docs[@]}"; do
  base="$(basename "$md" .md)"
  title="$(grep -m1 '^# ' "$md" | sed 's/^# //')"
  [ -n "$title" ] || { echo "render_docs: $base has no H1 title"; exit 1; }
  { printf '<!DOCTYPE html><html><head><meta charset="utf-8"><title>%s</title><style>' "$title"
    cat "$CSS"
    printf 'img.mermaid-img { display:block; margin:10px auto; border:1px solid #ddd; padding:6px; page-break-inside:avoid; }'
    printf '</style></head><body>'
    pandoc "$md" -f gfm -t html5
    printf '</body></html>'
  } > "$base.html"
  python3 imgfix.py "$base.html"
  # Page numbering comes from style.css's @page @bottom-center box, not from
  # CLI flags. WeasyPrint resolves local image refs relative to the input HTML.
  weasyprint --encoding utf-8 "$base.html" "$OUT/$base.pdf"
  echo "  rendered: $OUT/$base.pdf"
  count=$((count + 1))
done
echo "render_docs: $count document(s) → $OUT/"
