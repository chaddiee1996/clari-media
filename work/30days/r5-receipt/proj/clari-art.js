// clari-art.js: the Clari brand world for canvas reels and statics.
// Load after studio.js (needs nothing else). Everything is deterministic: pass seeds, never Math.random.
// All drawing functions take the 2D context first.
//
//   CLARI.sky(c, 'night'|'evening'|'dawn'|'day'|'icon', W, H)   full-frame sky gradient + moon glow
//   CLARI.stars(c, W, H, t, {seed, n, top, alpha})              twinkling stars (+ 4-point sparkles)
//   CLARI.moon(c, x, y, r, {glow, phase})                        the Clari crescent (same geometry as the logo)
//   CLARI.blossom(c, x, y, s, rot, {open})                       five-petal cherry blossom (open 0..1 to bloom)
//   CLARI.petal(c, x, y, s, rot, alpha)                          a single drifting petal
//   CLARI.branch(c, x, y, s, flip, t, {blossoms})               the app's blossom branch, swaying
//   CLARI.hills(c, W, H, variant, {y})                           layered hills at the bottom
//   CLARI.sparkle(c, x, y, s, alpha)                             4-point star
//   CLARI.phone(c, img, x, y, w, {rot, shadow})                 iPhone-style frame with a real app screen (img)
//   CLARI.plate(c, x, y, w, h, {fill, r})                        rounded caption plate
//   CLARI.rich(c, parts, x, y, {size, align, color, em})         one line of mixed type: [['Your ', 'b'], ['private', 'i'], ...]
//   CLARI.P palette, CLARI.F fonts
(function () {
  const TAU = Math.PI * 2;
  const P = {
    plum: '#4A2070', plumDeep: '#2A1548', night: '#22103F', violet: '#7A45B5', lilac: '#C3A8EA', tint: '#F1EAF7',
    cream: '#FFF8EC', paper: '#FBF6EE', pink: '#F7B6CD', blossom: '#E8628F', rose: '#B83A68', gold: '#FFE29A',
    ink: '#241A33', ink2: '#5F556B', moon0: '#FFFCF2', moon1: '#FFEFC9', moon2: '#F5C99E', peach: '#FFDDB5',
  };
  const F = { serif: "'Fraunces', serif", sans: "'Figtree', sans-serif", hand: "'Caveat', cursive" };
  // the app's four skies (from the app's SkyHeader), top -> bottom
  const SKIES = {
    night: ['#120723', '#2C1252', '#4A2180', '#6F3FA6', '#8E57BE'],
    evening: ['#150929', '#391766', '#7742AE', '#C47CBD', '#F7B9CB'],
    dawn: ['#3A2470', '#7A52B4', '#D58DB9', '#F8B7A9', '#FFDDB5'],
    day: ['#6B7BD8', '#9A90E2', '#C6A9EA', '#EBC6EA', '#FBE0EC'],
    icon: ['#7A45B5', '#6233A0', '#4A2180', '#331762', '#22103F'],
  };
  function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

  function sky(c, v, W, H, opts) {
    const o = Object.assign({ glowX: W * 0.72, glowY: H * 0.2, glowR: W * 0.9, glow: 0.22 }, opts || {});
    const s = SKIES[v] || SKIES.night;
    const g = v === 'icon' ? c.createLinearGradient(0, 0, W * 0.55, H) : c.createLinearGradient(0, 0, 0, H);
    [0, 0.36, 0.66, 0.86, 1].forEach((p, i) => g.addColorStop(p, s[i]));
    c.save(); c.globalAlpha = 1; c.fillStyle = g; c.fillRect(0, 0, W, H);
    if (o.glow > 0) {
      const r = c.createRadialGradient(o.glowX, o.glowY, 10, o.glowX, o.glowY, o.glowR);
      r.addColorStop(0, `rgba(249,201,216,${o.glow})`); r.addColorStop(0.5, `rgba(249,201,216,${o.glow * 0.4})`); r.addColorStop(1, 'rgba(249,201,216,0)');
      c.fillStyle = r; c.fillRect(0, 0, W, H);
    }
    c.restore();
  }
  const starCache = {};
  function stars(c, W, H, t, opts) {
    const o = Object.assign({ seed: 3, n: 140, top: 0, bottom: 0.7, alpha: 1, sparkles: 6 }, opts || {});
    const k = [o.seed, o.n, W, H].join();
    if (!starCache[k]) { const r = rng(o.seed); starCache[k] = Array.from({ length: o.n + o.sparkles }, () => [r() * W, H * (o.top + r() * (o.bottom - o.top)), 0.8 + r() * 2.0, r() * TAU, 0.35 + r() * 0.55, 0.9 + r() * 1.1]); }
    c.save(); c.fillStyle = '#FFFFFF';
    starCache[k].forEach(([x, y, rr, ph, a, sz], i) => {
      const al = o.alpha * a * (0.6 + 0.4 * Math.sin(t * 2.6 + ph));
      if (i < o.n) { c.globalAlpha = al; c.beginPath(); c.arc(x, y, rr, 0, TAU); c.fill(); }
      else sparkle(c, x, y, sz, al);
    });
    c.restore();
  }
  function sparkle(c, x, y, s, al) {
    c.save(); c.translate(x, y); c.scale(s, s); c.globalAlpha = al; c.fillStyle = '#FFF6DD';
    c.beginPath(); c.moveTo(0, -16); c.quadraticCurveTo(0, 0, 16, 0); c.quadraticCurveTo(0, 0, 0, 16); c.quadraticCurveTo(0, 0, -16, 0); c.quadraticCurveTo(0, 0, 0, -16); c.fill(); c.restore();
  }
  // crescent = disc minus an offset disc, exactly like the logo (offset +0.42r, -0.30r, cut radius 0.86r)
  function moon(c, x, y, r, opts) {
    const o = Object.assign({ glow: 1, cut: 1 }, opts || {});
    c.save();
    if (o.glow) {
      const g = c.createRadialGradient(x, y, r * 0.2, x, y, r * 2.4);
      g.addColorStop(0, `rgba(249,201,216,${0.45 * o.glow})`); g.addColorStop(0.5, `rgba(249,201,216,${0.14 * o.glow})`); g.addColorStop(1, 'rgba(249,201,216,0)');
      c.fillStyle = g; c.fillRect(x - r * 2.5, y - r * 2.5, r * 5, r * 5);
    }
    const off = document.createElement('canvas'); const S = Math.ceil(r * 2 + 8); off.width = off.height = S;
    const k = off.getContext('2d'); const cx = S / 2, cy = S / 2;
    const mg = k.createRadialGradient(cx - r * 0.3, cy - r * 0.4, r * 0.1, cx, cy, r * 1.1);
    mg.addColorStop(0, P.moon0); mg.addColorStop(0.55, P.moon1); mg.addColorStop(1, P.moon2);
    k.fillStyle = mg; k.beginPath(); k.arc(cx, cy, r, 0, TAU); k.fill();
    if (o.cut > 0) { k.globalCompositeOperation = 'destination-out'; k.beginPath(); k.arc(cx + r * 0.42 * o.cut, cy - r * 0.30 * o.cut, r * 0.86, 0, TAU); k.fill(); }
    c.drawImage(off, x - S / 2, y - S / 2); c.restore();
  }
  function petalPath(c) { c.beginPath(); c.moveTo(0, 0); c.bezierCurveTo(-17, -14, -19, -38, -5, -46); c.lineTo(0, -40); c.lineTo(5, -46); c.bezierCurveTo(19, -38, 17, -14, 0, 0); c.closePath(); }
  function blossom(c, x, y, s, rot, opts) {
    const o = Object.assign({ open: 1, alpha: 1 }, opts || {});
    const op = Math.max(0, Math.min(1, o.open));
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.globalAlpha = o.alpha;
    for (let i = 0; i < 5; i++) {
      c.save(); c.rotate(i * TAU / 5 + (1 - op) * 0.5); c.scale(0.55 + 0.45 * op, 0.55 + 0.45 * op);
      const g = c.createLinearGradient(0, -46, 0, 0); g.addColorStop(0, '#FFF0F5'); g.addColorStop(1, '#F28DB2');
      c.fillStyle = g; petalPath(c); c.fill(); c.restore();
    }
    if (op > 0.3) {
      c.globalAlpha = o.alpha * Math.min(1, (op - 0.3) / 0.5);
      for (let i = 0; i < 10; i++) {
        const a = (18 + 36 * i) * Math.PI / 180, ex = 18 * Math.cos(a), ey = 18 * Math.sin(a);
        c.strokeStyle = '#C2457A'; c.lineWidth = 2.4; c.beginPath(); c.moveTo(0, 0); c.lineTo(ex, ey); c.stroke();
        c.fillStyle = P.gold; c.beginPath(); c.arc(ex, ey, 3.6, 0, TAU); c.fill();
      }
    }
    c.globalAlpha = o.alpha; c.fillStyle = P.blossom; c.beginPath(); c.arc(0, 0, 9, 0, TAU); c.fill();
    c.restore();
  }
  function petal(c, x, y, s, rot, al) {
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * 0.6, s * 0.6); c.globalAlpha = al == null ? 1 : al;
    const g = c.createLinearGradient(0, -46, 0, 0); g.addColorStop(0, '#FFF0F5'); g.addColorStop(1, '#F28DB2');
    c.fillStyle = g; petalPath(c); c.fill(); c.restore();
  }
  // the app's branch (drawn at 1 unit = 1 px of a 390 pt wide phone; scale s ~ 2.8 for a 1080 frame)
  function branch(c, x, y, s, flip, t, opts) {
    const o = Object.assign({ blossoms: 7, sway: 1 }, opts || {});
    c.save(); c.translate(x, y); c.scale(flip ? -s : s, s); c.rotate(0.015 * o.sway * Math.sin((t || 0) * 1.1));
    c.lineCap = 'round';
    const paths = [['M-8 22 C30 32 70 26 112 44 C136 54 156 58 182 52', 3.2], ['M56 29 C72 46 84 58 90 80', 2.3], ['M112 44 C124 36 138 28 154 26', 2], ['M24 28 C29 42 29 56 22 70', 1.9], ['M146 54 C154 62 160 70 162 82', 1.6]];
    paths.forEach(([d, w], i) => { const p = new Path2D(d); if (i === 0) { c.strokeStyle = 'rgba(42,18,69,0.55)'; c.lineWidth = 5.4; c.stroke(p); } c.strokeStyle = '#B89AD8'; c.lineWidth = w; c.stroke(p); });
    const pos = [[36, 29, 1.55, 10], [91, 82, 1.7, 24], [154, 25, 1.5, 12], [22, 72, 1.35, 34], [182, 52, 1.3, 58], [82, 44, 1.2, 44], [162, 84, 1.15, 70]];
    pos.forEach(([bx, by, bs, br], i) => {
      if (i < o.blossoms) blossom(c, bx, by, bs * 0.29, br * Math.PI / 180, { open: o.open == null ? 1 : Math.max(0, Math.min(1, o.open * 7 - i)) });
      else { c.fillStyle = '#F39BB9'; c.beginPath(); c.ellipse(bx, by, 2.6, 3.6, br * Math.PI / 180, 0, TAU); c.fill(); }
    });
    c.restore();
  }
  function hills(c, W, H, v, opts) {
    const o = Object.assign({ y: 0 }, opts || {}); const h = H + o.y;
    const back = v === 'day' ? 'rgba(160,140,220,0.55)' : v === 'dawn' ? 'rgba(122,82,180,0.55)' : 'rgba(108,58,168,0.6)';
    const front = v === 'day' ? 'rgba(120,96,196,0.6)' : 'rgba(59,24,104,0.75)';
    c.save(); c.fillStyle = back; c.beginPath(); c.moveTo(0, h - 260);
    c.bezierCurveTo(W * 0.16, h - 380, W * 0.3, h - 300, W * 0.44, h - 330); c.bezierCurveTo(W * 0.6, h - 370, W * 0.74, h - 450, W, h - 340); c.lineTo(W, h); c.lineTo(0, h); c.fill();
    c.fillStyle = front; c.beginPath(); c.moveTo(0, h - 170); c.bezierCurveTo(W * 0.2, h - 260, W * 0.36, h - 150, W * 0.56, h - 210); c.bezierCurveTo(W * 0.72, h - 265, W * 0.86, h - 250, W, h - 196); c.lineTo(W, h); c.lineTo(0, h); c.fill();
    c.restore();
  }
  function rr(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
  // phone frame: img should be a real app screenshot (kit/screens, 1290 x 2796). x,y = centre.
  function phone(c, img, x, y, w, opts) {
    const o = Object.assign({ rot: 0, shadow: 1, crop: 0 }, opts || {});
    const h = w * 2796 / 1290, bez = w * 0.035, R = w * 0.16;
    c.save(); c.translate(x, y); c.rotate(o.rot);
    if (o.shadow) { c.shadowColor = 'rgba(16,4,40,0.5)'; c.shadowBlur = w * 0.18; c.shadowOffsetY = w * 0.08; }
    c.fillStyle = '#16101F'; rr(c, -w / 2 - bez, -h / 2 - bez, w + bez * 2, h + bez * 2, R + bez); c.fill();
    c.shadowColor = 'transparent';
    c.save(); rr(c, -w / 2, -h / 2, w, h, R); c.clip();
    if (img && img.complete && img.naturalWidth) c.drawImage(img, -w / 2, -h / 2, w, h); else { c.fillStyle = P.night; c.fillRect(-w / 2, -h / 2, w, h); }
    c.restore();
    c.strokeStyle = 'rgba(255,255,255,0.14)'; c.lineWidth = Math.max(1, w * 0.004); rr(c, -w / 2 - bez * 0.5, -h / 2 - bez * 0.5, w + bez, h + bez, R + bez * 0.5); c.stroke();
    c.restore();
  }
  function plate(c, x, y, w, h, opts) {
    const o = Object.assign({ fill: 'rgba(34,16,63,0.82)', r: 28 }, opts || {});
    c.save(); c.fillStyle = o.fill; rr(c, x, y, w, h, o.r); c.fill(); c.restore();
  }
  // mixed-type line. parts: [[text, 'b'|'i'|'s'], ...] b = Fraunces 700, i = Fraunces italic in em colour, s = Figtree 700
  function rich(c, parts, x, y, opts) {
    const o = Object.assign({ size: 120, align: 'center', color: P.cream, em: P.pink, weight: 700 }, opts || {});
    const font = k => k === 'i' ? `italic 600 ${o.size}px ${F.serif}` : k === 's' ? `700 ${o.size}px ${F.sans}` : `${o.weight} ${o.size}px ${F.serif}`;
    let total = 0; const ws = parts.map(([tx, k]) => { c.font = font(k); const w = c.measureText(tx).width; total += w; return w; });
    let cx = o.align === 'center' ? x - total / 2 : o.align === 'right' ? x - total : x;
    c.save(); c.textAlign = 'left'; c.textBaseline = 'alphabetic';
    parts.forEach(([tx, k], i) => { c.font = font(k); c.fillStyle = k === 'i' ? o.em : o.color; c.fillText(tx, cx, y); cx += ws[i]; });
    c.restore(); return total;
  }
  function loadImg(src) { const i = new Image(); i.src = src; return i; }
  window.CLARI = { P, F, SKIES, rng, sky, stars, sparkle, moon, blossom, petal, branch, hills, phone, plate, rich, rr, loadImg };
})();
