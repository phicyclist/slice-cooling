import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer-core';
import fs from 'fs'; import path from 'path';
const [,, inDir, outDir] = process.argv;
fs.mkdirSync(outDir, { recursive: true });
const mermaidJs = fs.readFileSync('node_modules/mermaid/dist/mermaid.min.js', 'utf8');
const browser = await puppeteer.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: 'shell' });
const page = await browser.newPage();
await page.setViewport({ width: 2600, height: 2000, deviceScaleFactor: 2 });
await page.setContent('<html><head><style>body{margin:0;padding:14px;background:#fff}#d{display:inline-block}</style></head><body><div id="d"></div></body></html>');
await page.addScriptTag({ content: mermaidJs });
await page.evaluate(() => mermaid.initialize({
  startOnLoad: false, theme: 'neutral', securityLevel: 'loose',
  flowchart: { htmlLabels: true, curve: 'basis', useMaxWidth: false },
  state: { useMaxWidth: false }, sequence: { useMaxWidth: false },
  themeVariables: { fontFamily: 'sans-serif', fontSize: '15px' }
}));
for (const f of fs.readdirSync(inDir).filter(f => f.endsWith('.mmd')).sort()) {
  const src = fs.readFileSync(path.join(inDir, f), 'utf8');
  try {
    const dims = await page.evaluate(async (s) => {
      const { svg } = await mermaid.render('g' + Math.random().toString(36).slice(2), s);
      const d = document.getElementById('d'); d.innerHTML = svg;
      const el = d.querySelector('svg');
      el.style.maxWidth = 'none';
      const bb = el.getBoundingClientRect();
      return [Math.ceil(bb.width), Math.ceil(bb.height)];
    }, src);
    const el = await page.$('#d');
    await el.screenshot({ path: path.join(outDir, f.replace(/\.mmd$/, '.png')) });
    console.log('ok', f, dims[0] + 'x' + dims[1]);
  } catch (e) { console.error('FAIL', f, String(e).slice(0, 150)); }
}
await browser.close();
