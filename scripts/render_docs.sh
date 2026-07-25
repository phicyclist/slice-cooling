#!/usr/bin/env bash
# render_docs.sh v2 — lineage docs → PDF with rendered Mermaid diagrams
# Pipeline: preprocess.py (mermaid → PNG refs) → mmrender.mjs (Chromium via
# @sparticuz/chromium + mermaid.js → 2x PNG) → pandoc → imgfix.py → wkhtmltopdf.
# Ultra-wide diagrams (>1600 CSS px) are rotated 90° as full-height figures. MIT.
set -euo pipefail
SRC="${1:-md_pre}"; OUT="${2:-out3}"; CSS="style.css"
mkdir -p "$OUT"
for md in "$SRC"/[0-9][0-9]_*.md; do
  base="$(basename "$md" .md)"
  title="$(grep -m1 '^# ' "$md" | sed 's/^# //')"
  { printf '<!DOCTYPE html><html><head><meta charset="utf-8"><title>%s</title><style>' "$title"
    cat "$CSS"
    printf 'img.mermaid-img { display:block; margin:10px auto; border:1px solid #ddd; padding:6px; page-break-inside:avoid; }'
    printf '</style></head><body>'
    pandoc "$md" -f gfm -t html5
    printf '</body></html>'
  } > "$base.html"
  python3 imgfix.py "$base.html"
  wkhtmltopdf --enable-local-file-access --quiet \
    --footer-center '[page]/[topage]' --footer-font-size 7 --footer-spacing 4 \
    "$base.html" "$OUT/$base.pdf"
  echo "  rendered: $OUT/$base.pdf"
done
