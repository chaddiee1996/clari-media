// type.js: DOM headline blocks that rise through masks, driven only from t (no timers).
// TYPE.block(parent, 'line one|line <i>two</i>', {left, top, width, size, lh, align, cls})
// TYPE.show(block, t, tIn, tOut, {stag, dur, ease, outDur, dy})
(function () {
  function block(parent, html, o) {
    o = Object.assign({ left: 0, top: 0, width: 1080, size: 120, lh: 1.05, align: 'center', cls: 'serif' }, o || {});
    const el = document.createElement('div');
    el.className = 'tblock ' + o.cls;
    Object.assign(el.style, { left: o.left + 'px', top: o.top + 'px', width: o.width + 'px', fontSize: o.size + 'px',
      lineHeight: o.lh, textAlign: o.align, visibility: 'hidden' });
    const lines = html.split('|').map(h => {
      const ln = document.createElement('div'); ln.className = 'ln';
      const inn = document.createElement('span'); inn.className = 'in'; inn.innerHTML = h;
      ln.appendChild(inn); el.appendChild(ln); return inn;
    });
    parent.appendChild(el);
    return { el, lines };
  }
  function show(b, t, tIn, tOut, o) {
    o = Object.assign({ stag: 0.07, dur: 0.75, ease: 'expo.out', outDur: 0.28, dy: 1.15, outDy: 70 }, o || {});
    const S = window.STUDIO;
    const vis = t >= tIn - 0.001 && (tOut == null || t < tOut + o.outDur + 0.05 * b.lines.length);
    b.el.style.visibility = vis ? 'visible' : 'hidden';
    if (!vis) return 0;
    let last = 0;
    b.lines.forEach((inn, i) => {
      const pi = S.seg(t, tIn + i * o.stag, o.dur, o.ease);
      const po = tOut == null ? 0 : S.seg(t, tOut + i * 0.035, o.outDur, 'power2.in');
      inn.style.transform = `translateY(${(1 - pi) * o.dy * 100}%) translateY(${-po * o.outDy}px)`;
      inn.style.opacity = 1 - po;
      last = pi;
    });
    return last;
  }
  window.TYPE = { block, show };
})();
