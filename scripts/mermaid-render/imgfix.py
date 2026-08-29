# Diagram width cap is 540 CSS px, proportioned to style.css's 8pt type ladder.
# It was 680 under wkhtmltopdf, which down-scaled the whole page ~25%; at true
# scale 680px overruns the text block and pushes figures onto their own page.
#
# Height is capped too (v1.6): the A4 text block at 11mm margins is ~1040 CSS px,
# and an inline figure taller than that cannot fit on ANY page — WeasyPrint clips
# it silently. The own-page branch only catches figures above 1600 CSS px, so the
# 1040–1600 band overflowed with no warning; doc 00's figure 4.1 hit it in an
# intermediate draft and was caught only by hand-measuring. Anything scaled down
# for height is reported on stderr so the render log shows it happened.
import re, sys
from PIL import Image
MAX_W, MAX_H = 540, 900   # display CSS px; MAX_H leaves room for border+margins
p = sys.argv[1]; h = open(p).read()
def fix(m):
    src = m.group(1)
    im = Image.open(src); w, hh = im.size            # device px (2x render)
    rotate = w > hh and w // 2 > 1600
    if rotate:
        im.transpose(Image.ROTATE_90).save(src)
    if rotate or hh // 2 > 1600:                     # tall figure: own page
        return ('<div style="page-break-before:always;page-break-after:always;'
                'text-align:center;">'
                f'<img src="{src}" class="mermaid-img" style="height:840px;width:auto;" alt=""/></div>')
    cw, ch = w // 2, hh // 2
    disp_w = min(cw, MAX_W)
    if ch * disp_w / cw > MAX_H:                     # would overflow the text block
        disp_w = int(cw * MAX_H / ch)
        print(f"imgfix: {src} scaled to {disp_w}px wide to fit page height "
              f"({cw}x{ch} CSS px source)", file=sys.stderr)
    return f'<img src="{src}" class="mermaid-img" style="width:{disp_w}px;max-width:100%;" alt=""/>'
h = re.sub(r'<img src="(mmpng/[^"]+)"[^>]*/?>', fix, h)
open(p, 'w').write(h)
