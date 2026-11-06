// usage: node shot.js <file.html|svg> <out.png> <width> <height> [scale]
const { chromium } = require('playwright');
(async () => {
  const [f, out, w, h, s] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +(s || 1) });
  await p.goto('file://' + require('path').resolve(f));
  await p.evaluate(() => document.fonts && document.fonts.ready);
  await p.waitForTimeout(400);
  await p.screenshot({ path: out, omitBackground: true });
  await b.close();
})();
