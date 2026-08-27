# Extracts ```mermaid blocks to .mmd and rewrites the markdown to reference the
# rendered PNGs. Processes EVERY .md in the source directory: the doc set is not
# uniformly numbered (executive_summary.md carries diagrams too), and a narrower
# glob silently ships un-rendered code fences instead of figures. Keep this glob
# and render_docs.sh's in agreement.
import re, sys, pathlib
src, mmd_dir, md_out = map(pathlib.Path, sys.argv[1:4])
mmd_dir.mkdir(exist_ok=True); md_out.mkdir(exist_ok=True)
pat = re.compile(r'```mermaid\n(.*?)```', re.S)
sources = sorted(src.glob('*.md'))
if not sources:
    sys.exit(f'preprocess: no .md files found in {src}')
for f in sources:
    i = 0
    def sub(m):
        global i
        i += 1
        name = f"{f.stem}_{i:02d}"
        (mmd_dir / f"{name}.mmd").write_text(m.group(1))
        return f'![](mmpng/{name}.png)'
    out = pat.sub(sub, f.read_text())
    (md_out / f.name).write_text(out)
    print(f"{f.name}: {i} diagram(s)")
