import re, sys
from PIL import Image
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
    return f'<img src="{src}" class="mermaid-img" style="width:{min(w // 2, 680)}px;max-width:100%;" alt=""/>'
h = re.sub(r'<img src="(mmpng/[^"]+)"[^>]*/?>', fix, h)
open(p, 'w').write(h)
