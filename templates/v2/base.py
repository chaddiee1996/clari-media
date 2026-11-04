"""Shared renderer for Clari v2 content. Each post module provides slides(kind) -> (css, [body html]).
Sizes: ig 1080x1440 (3:4 feed), tt 1080x1920 (TikTok photo), st 1080x1920 (story).
Every page is checked for clipped text, text outside the platform safe area, text overlapping text,
and text sitting on top of images, before it is saved."""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SIZES = {"ig": (1080, 1440), "tt": (1080, 1920), "st": (1080, 1920)}
# left, top, right, bottom margins that text must stay inside
SAFE = {"ig": (56, 56, 56, 56), "tt": (60, 150, 150, 430), "st": (60, 230, 60, 340)}

def U(p):
    return (HERE / p).as_uri()

FONTS = f"""
@font-face{{font-family:Brico;src:url({U('fonts/bricolage.woff2')});font-weight:200 800;font-stretch:75% 100%}}
@font-face{{font-family:Archivo;src:url({U('fonts/archivo.woff2')});font-weight:100 900;font-stretch:62% 125%}}
@font-face{{font-family:Kalam;src:url({U('fonts/kalam-400.woff2')});font-weight:400}}
@font-face{{font-family:Kalam;src:url({U('fonts/kalam-700.woff2')});font-weight:700}}
@font-face{{font-family:Typer;src:url({U('fonts/special-elite.woff2')})}}
@font-face{{font-family:Fig;src:url({U('fonts/figtree.woff2')});font-weight:300 900}}
@font-face{{font-family:Mono;src:url({U('fonts/dm-mono-400.woff2')});font-weight:400}}
@font-face{{font-family:Mono;src:url({U('fonts/dm-mono-500.woff2')});font-weight:500}}
@font-face{{font-family:Frau;src:url({U('fonts/fraunces-full.woff2')});font-weight:100 900}}
@font-face{{font-family:Frau;src:url({U('fonts/fraunces-full-italic.woff2')});font-weight:100 900;font-style:italic}}
"""

RESET = """*{margin:0;padding:0;box-sizing:border-box}
html,body{width:Wpx;height:Hpx;overflow:hidden}
.c{position:relative;width:Wpx;height:Hpx;overflow:hidden;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
"""

def page(w, h, css, body, kind):
    r = RESET.replace("Wpx", f"{w}px").replace("Hpx", f"{h}px")
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTS}{r}{css}</style></head>"
            f"<body data-kind='{kind}' data-safe='{json.dumps(SAFE[kind])}'><div class='c'>{body}</div></body></html>")

def mark(color="#FFF3D6", size=40):
    svg = (HERE / "mark-moon.svg").read_text()
    return f'<span class="mk" style="display:inline-block;width:{size}px;height:{size}px;color:{color}">{svg}</span>'

CHECK_JS = r"""
() => {
  const W = innerWidth, H = innerHeight, kind = document.body.dataset.kind;
  const S = JSON.parse(document.body.dataset.safe);
  const bad = [];
  // overlap and clipping are judged with rotations removed, so tilted cards don't give false alarms
  const tilted = [...document.querySelectorAll('.tag,.note,.rot')];
  const saved = tilted.map(t => t.style.transform);
  const measure = () => [...document.querySelectorAll('body *')].filter(x => !x.closest('.deco') &&
      [...x.childNodes].some(c => c.nodeType === 3 && c.textContent.trim())).map(x => { if (getComputedStyle(x).display !== 'inline') return [x, [x.getBoundingClientRect()]]; const r = document.createRange(); r.selectNodeContents(x); return [x, [...r.getClientRects()].filter(b => b.width > 1)]; });
  tilted.forEach(t => t.style.transform = 'none');
  const flat = measure();
  tilted.forEach((t, i) => t.style.transform = saved[i]);
  const holders = [...document.querySelectorAll('body *')].filter(x => !x.closest('.deco') &&
      [...x.childNodes].some(c => c.nodeType === 3 && c.textContent.trim()));
  const rects = holders.map(x => { const r = document.createRange(); r.selectNodeContents(x); return [x, [...r.getClientRects()].filter(b => b.width > 1)]; });
  for (const [x, A] of rects) {
    const cs = getComputedStyle(x); if (cs.visibility === 'hidden' || cs.opacity === '0') continue;
    for (const b of A) {
      const rlim = (kind === 'tt' && b.bottom < 700) ? 60 : S[2];
      if (b.left < S[0] - 2 || b.top < S[1] - 2 || b.right > W - rlim + 2 || b.bottom > H - S[3] + 2)
        bad.push(`unsafe "${x.textContent.trim().slice(0, 36)}" ${Math.round(b.left)},${Math.round(b.top)},${Math.round(b.right)},${Math.round(b.bottom)}`);
    }
    let a = x;
    while (a && a !== document.body) {
      const s = getComputedStyle(a);
      if (s.overflow !== 'visible' && !a.classList.contains('c') && (a.scrollHeight > a.clientHeight + 1 || a.scrollWidth > a.clientWidth + 1))
        bad.push(`clipped in .${a.className}: "${x.textContent.trim().slice(0, 36)}"`);
      a = a.parentElement;
    }
  }
  for (let i = 0; i < flat.length; i++) for (let j = i + 1; j < flat.length; j++) {
    const [x, A] = flat[i], [y, B] = flat[j];
    if (x.contains(y) || y.contains(x) || x.closest('.ok') || y.closest('.ok')) continue;
    for (const a of A) for (const b of B) {
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 3 && oy > 3) bad.push(`overlap "${x.textContent.trim().slice(0, 28)}" / "${y.textContent.trim().slice(0, 28)}"`);
    }
  }
  const objs = [...document.querySelectorAll('.obj')];
  for (const [x, A] of rects) for (const o of objs) {
    if (o.contains(x) || x.closest('.ok')) continue;
    const b = o.getBoundingClientRect();
    for (const a of A) {
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 3 && oy > 3) bad.push(`text on object: "${x.textContent.trim().slice(0, 28)}"`);
    }
  }
  return [...new Set(bad)];
}
"""

def render(name, fn, out, kinds=("ig", "tt"), scale=1):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    tmp = HERE / f"_{name}.html"
    problems, files = [], []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for kind in kinds:
            w, h = SIZES[kind]
            css, slides = fn(kind)
            pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
            for i, body in enumerate(slides):
                tmp.write_text(page(w, h, css, body, kind))
                pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
                problems += [f"{name} {kind} {i + 1}: {m}" for m in pg.evaluate(CHECK_JS)]
                f = out / f"{name}-{kind}-{i + 1:02d}.png"
                pg.screenshot(path=str(f)); files.append(f)
            pg.close()
        b.close()
    tmp.unlink(missing_ok=True)
    print("\n".join(problems) or f"{name}: all clear")
    return files, problems
