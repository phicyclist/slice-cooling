import re, sys, pathlib
src, mmd_dir, md_out = map(pathlib.Path, sys.argv[1:4])
mmd_dir.mkdir(exist_ok=True); md_out.mkdir(exist_ok=True)
pat = re.compile(r'```mermaid\n(.*?)```', re.S)
for f in sorted(src.glob('[0-9][0-9]_*.md')):
    i = 0
    def sub(m):
        global i
        i += 1
        name = f"{f.stem}_{i:02d}"
        (mmd_dir / f"{name}.mmd").write_text(m.group(1))
        return f'![](mmpng/{name}.png)'
    out = pat.sub(sub, f.read_text())
    (md_out / f.name).write_text(out)
    if i: print(f.name, i, 'diagram(s)')
