// fx.js: shared helpers for the R9..R13 reels (load after studio.js and clari-art.js).
// Deterministic only. All text is drawn on canvas with Fraunces / Figtree.
(function () {
  const TAU = Math.PI * 2, S = window.STUDIO, P = window.CLARI.P;
  const cl = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, p) => a + (b - a) * p;
  const E = (n) => S.ease(n);
  // eased progress, clamped
  const seg = (t, a, d, e) => S.seg(t, a, d, e || 'power3.out');
  // in/out envelope: 0 before a, 1 between, 0 after b (with its own eases)
  const env = (t, a, din, b, dout, ein, eout) => seg(t, a, din, ein || 'expo.out') * (1 - seg(t, b, dout, eout || 'power2.in'));

  function font(kind, size, weight) {
    if (kind === 'i') return `italic ${weight || 600} ${size}px 'Fraunces', serif`;
    if (kind === 's') return `${weight || 800} ${size}px 'Figtree', sans-serif`;
    if (kind === 'h') return `${weight || 700} ${size}px 'Caveat', cursive`;
    return `${weight || 700} ${size}px 'Fraunces', serif`;
  }
  // split parts [[text, kind], ...] into words keeping kind; returns [{w, k, x, width}]
  function layoutLine(c, parts, size, weight) {
    const words = [];
    parts.forEach(([tx, k]) => {
      const bits = tx.split(/(\s+)/).filter(b => b.length);
      bits.forEach(b => words.push({ w: b, k }));
    });
    let x = 0;
    words.forEach(o => { c.font = font(o.k, size, o.k === 's' ? (weight && weight.s) : (weight && weight.b)); o.width = c.measureText(o.w).width; o.x = x; x += o.width; });
    return { words, width: x };
  }
  // Text block with a masked word-by-word rise in, and a rise-out.
  // spec: {lines:[parts...], x, y (first baseline), size, lh, align:'left'|'center'|'right', color, em,
  //        tin, tout, stagger, dur, rise, mask:true, alpha, weight:{b,s}, shadow}
  function text(c, spec, t) {
    const o = Object.assign({ align: 'center', color: P.cream, em: P.pink, lh: 1.08, stagger: 0.055, dur: 0.75, rise: 1.0,
      tout: 1e9, outDur: 0.42, mask: true, alpha: 1, ein: 'expo.out', eout: 'power3.in', shadow: 0.35 }, spec);
    if (t < o.tin - 0.01 || t > o.tout + o.outDur + 0.5) return;
    const size = o.size, lh = size * o.lh;
    let wi = 0;
    c.save();
    o.lines.forEach((parts, li) => {
      const lsize = (o.sizes && o.sizes[li]) || size;
      const L = layoutLine(c, parts, lsize, o.weight);
      const by = o.y + (o.lineY ? o.lineY[li] : li * lh);
      const x0 = o.align === 'center' ? o.x - L.width / 2 : o.align === 'right' ? o.x - L.width : o.x;
      L.words.forEach((wd) => {
        if (!wd.w.trim()) return;
        const st = o.times ? o.times[Math.min(wi, o.times.length - 1)] : o.tin + wi * o.stagger; wi++;
        const pin = seg(t, st, o.dur, o.ein);
        const pout = seg(t, o.tout + (wi - 1) * o.stagger * 0.5, o.outDur, o.eout);
        if (pin <= 0 || pout >= 1) return;
        const dy = (1 - pin) * lsize * o.rise - pout * lsize * 0.7;
        c.save();
        if (o.mask) { c.beginPath(); c.rect(x0 + wd.x - lsize, by - lsize * 1.05, wd.width + lsize * 2, lsize * 1.45); c.clip(); }
        c.globalAlpha = o.alpha * Math.min(1, pin * 1.6) * (1 - pout);
        c.font = font(wd.k, lsize, wd.k === 's' ? (o.weight && o.weight.s) : (o.weight && o.weight.b));
        c.textAlign = 'left'; c.textBaseline = 'alphabetic';
        if (o.shadow) { c.shadowColor = `rgba(16,4,40,${o.shadow})`; c.shadowBlur = lsize * 0.25; c.shadowOffsetY = lsize * 0.06; }
        c.fillStyle = wd.k === 'i' ? o.em : (o.colorS && wd.k === 's' ? o.colorS : o.color);
        c.fillText(wd.w, x0 + wd.x, by + dy);
        c.restore();
      });
    });
    c.restore();
  }
  function width(c, parts, size, weight) { return layoutLine(c, parts, size, weight).width; }
  // Text along a circle above a centre (reads left to right, clockwise). ang = centre angle (rad), -PI/2 = top.
  // p: 0..1 per-letter reveal (letters swing in along the arc), q: 0..1 exit (letters swing on and fade).
  function arcText(c, parts, cx, cy, r, ang, size, o) {
    o = Object.assign({ color: P.cream, em: P.pink, p: 1, q: 0, swing: 0.32, shadow: 0.4, weight: 700, spread: 1 }, o || {});
    // character list with kerned advances
    const chars = [];
    let total = 0;
    parts.forEach(([tx, k]) => {
      c.font = font(k, size, o.weight);
      for (let i = 0; i < tx.length; i++) {
        const a = c.measureText(tx.slice(0, i)).width, b = c.measureText(tx.slice(0, i + 1)).width;
        chars.push({ ch: tx[i], k, x: total + a, w: b - a });
      }
      total += c.measureText(tx).width;
    });
    total *= o.spread;
    const span = total / r; const a0 = ang - span / 2;
    const n = chars.length;
    c.save(); c.textAlign = 'center'; c.textBaseline = 'alphabetic';
    chars.forEach((ch, i) => {
      if (ch.ch === ' ') return;
      const f = n > 1 ? i / (n - 1) : 0;
      // staggered letter progress
      const pi = cl(o.p * 1.6 - f * 0.6, 0, 1), qi = cl(o.q * 1.6 - f * 0.6, 0, 1);
      const ei = E('expo.out')(pi), eq = E('power2.in')(qi);
      if (ei <= 0 || eq >= 1) return;
      const a = a0 + (ch.x * o.spread + ch.w / 2) / r - (1 - ei) * o.swing + eq * o.swing;
      c.save(); c.translate(cx + Math.cos(a) * r, cy + Math.sin(a) * r); c.rotate(a + Math.PI / 2);
      c.globalAlpha = (o.alpha == null ? 1 : o.alpha) * ei * (1 - eq);
      c.font = font(ch.k, size, o.weight);
      if (o.shadow) { c.shadowColor = `rgba(16,4,40,${o.shadow})`; c.shadowBlur = size * 0.22; c.shadowOffsetY = size * 0.05; }
      c.fillStyle = ch.k === 'i' ? o.em : o.color;
      c.fillText(ch.ch, 0, 0); c.restore();
    });
    c.restore();
    return span;
  }
  function rr(c, x, y, w, h, r) { CLARI.rr(c, x, y, w, h, Math.min(r, w / 2, h / 2)); }
  function shadow(c, blur, oy, a) { c.shadowColor = `rgba(16,4,40,${a == null ? 0.35 : a})`; c.shadowBlur = blur; c.shadowOffsetY = oy || 0; c.shadowOffsetX = 0; }
  function noShadow(c) { c.shadowColor = 'transparent'; c.shadowBlur = 0; c.shadowOffsetY = 0; }
  function vgrad(c, y0, y1, stops) { const g = c.createLinearGradient(0, y0, 0, y1); stops.forEach((s, i) => g.addColorStop(s[0], s[1])); return g; }
  function rgrad(c, x, y, r0, r1, stops) { const g = c.createRadialGradient(x, y, r0, x, y, r1); stops.forEach(s => g.addColorStop(s[0], s[1])); return g; }
  // frost: dendrite segments growing from seeds along rectangle edges. returns segments [x1,y1,x2,y2,birth,w]
  function frostMake(seed, rect, n) {
    const r = CLARI.rng(seed), segs = [];
    const [X, Y, Wd, Ht] = rect;
    function grow(x, y, a, len, depth, b0, w) {
      const steps = 5 + Math.floor(r() * 3); let px = x, py = y; const sl = len / steps;
      for (let i = 0; i < steps; i++) {
        a += (r() - 0.5) * 0.25;
        const nx = px + Math.cos(a) * sl, ny = py + Math.sin(a) * sl;
        const b = b0 + (i + 1) / steps * (1 - b0) * (0.55 + depth * 0.12);
        segs.push([px, py, nx, ny, Math.min(1, b0 + (b - b0)), w]);
        if (depth < 2 && i > 0 && r() < 0.75) {
          const side = (r() < 0.5 ? -1 : 1) * (0.9 + r() * 0.3);
          grow(px, py, a + side, len * (0.35 + r() * 0.2), depth + 1, Math.min(1, b0 + (b - b0) * 0.8), w * 0.65);
          if (r() < 0.5) grow(px, py, a - side, len * (0.3 + r() * 0.2), depth + 1, Math.min(1, b0 + (b - b0) * 0.8), w * 0.65);
        }
        px = nx; py = ny;
      }
    }
    for (let i = 0; i < n; i++) {
      const e = Math.floor(r() * 4), u = r();
      let x, y, a;
      if (e === 0) { x = X + u * Wd; y = Y; a = Math.PI / 2; }
      else if (e === 1) { x = X + u * Wd; y = Y + Ht; a = -Math.PI / 2; }
      else if (e === 2) { x = X; y = Y + u * Ht; a = 0; }
      else { x = X + Wd; y = Y + u * Ht; a = Math.PI; }
      // corners grow more
      const cornerish = Math.min(u, 1 - u) < 0.2 ? 1.5 : 1;
      grow(x, y, a + (r() - 0.5) * 1.1, (60 + r() * 120) * cornerish, 0, r() * 0.35, 3.2);
    }
    return segs;
  }
  function frostDraw(c, segs, f, alpha) {
    if (f <= 0) return;
    c.save(); c.lineCap = 'round'; c.strokeStyle = '#F4F1FF';
    segs.forEach(([x1, y1, x2, y2, b, w]) => {
      if (b > f) return;
      const g = cl((f - b) / 0.08, 0, 1);
      c.globalAlpha = alpha * (0.35 + 0.4 * (w / 3.2));
      c.lineWidth = w; c.beginPath(); c.moveTo(x1, y1); c.lineTo(lerp(x1, x2, g), lerp(y1, y2, g)); c.stroke();
    });
    c.restore();
  }
  // simple 1D value noise
  function noise1(x, seed) { const i = Math.floor(x), f = x - i; const h = (n) => { const s = Math.sin((n + (seed || 0) * 57.3) * 127.1) * 43758.5453; return s - Math.floor(s); }; const u = f * f * (3 - 2 * f); return lerp(h(i), h(i + 1), u); }
  window.FX = { TAU, cl, lerp, seg, env, font, text, width, arcText, rr, shadow, noShadow, vgrad, rgrad, frostMake, frostDraw, noise1, layoutLine };
})();
