// usage: node render.js jobs.json
// jobs: [{html, w, h, slides:[{i, out}]}]. One browser, one page, sequential (2 CPUs shared with reel builders).
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const path = require('path');
(async () => {
  const jobs = require(path.resolve(process.argv[2]));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1440 } });
  p.on('pageerror', e => console.error('PAGEERROR', e.message));
  for (const j of jobs) {
    await p.setViewportSize({ width: j.w, height: j.h });
    await p.goto('file://' + path.resolve(j.html));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForFunction(() => window.__ready === true, null, { timeout: 30000 }).catch(() => console.error('not ready', j.html));
    await p.waitForTimeout(150);
    for (const s of j.slides) {
      await p.evaluate(i => window.show(i), s.i);
      await p.waitForTimeout(60);
      await p.screenshot({ path: s.out });
      console.log(s.out);
    }
  }
  await b.close();
})();
