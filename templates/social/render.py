"""Clari social renderer (November 2026 system).

python3 render.py content.json OUTDIR [--sizes ig,tt,story]

Art direction: night and dawn pages from a moonlit diary. One signature
element only: the moon, which fills as you move through a carousel (the
same way it fills in the app as a symptom gets stronger). Type does the
rest. No eyebrow labels, no decorative numbering, no glass cards, no
single-word colour accents.
"""
import json, math, sys, pathlib, html
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SIZES = {"ig": (1080, 1350), "tt": (1080, 1920), "story": (1080, 1920)}

def esc(t):
    return html.escape(t or "").replace("|", "<br>")

def rnd(i):
    x = math.sin(i * 127.1 + 311.7) * 43758.5453
    return x - math.floor(x)

def stars(w, h, seed=3, n=46):
    out = []
    for i in range(n):
        x = rnd(i + seed) * w; y = rnd(i + 400 + seed) * h * 0.34
        r = 0.8 + rnd(i + 900) * 1.6; o = 0.2 + rnd(i + 41) * 0.55
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#FFF3D6" opacity="{o:.2f}"/>')
    return f'<svg class="stars" width="{w}" height="{h}">{"".join(out)}</svg>'

def moon(fill, size=104, dark=True):
    """Phase moon: lit part grows from a thin crescent (fill 0) to full (fill 1)."""
    off = 30 + fill * 80
    ring = "rgba(255,243,214,.22)" if dark else "rgba(36,16,63,.30)"
    disc = "rgba(255,243,214,.06)" if dark else "rgba(36,16,63,.10)"
    return f'''<svg class="pmoon" viewBox="0 0 100 100" width="{size}" height="{size}">
<defs><radialGradient id="mg" cx="0.35" cy="0.3" r="0.9"><stop offset="0" stop-color="#FFFBEE"/>
<stop offset="0.6" stop-color="#FFEFC9"/><stop offset="1" stop-color="#F3CDA6"/></radialGradient>
<mask id="mm"><rect width="100" height="100" fill="#fff"/><circle cx="{50 + off:.1f}" cy="46" r="42" fill="#000"/></mask></defs>
<circle cx="50" cy="50" r="42" fill="{disc}" stroke="{ring}" stroke-width="2"/>
<circle cx="50" cy="50" r="42" fill="url(#mg)" mask="url(#mm)"/></svg>'''

def moon_row(total, lit, dark=True):
    cells = []
    for i in range(total):
        on = i < lit
        fill = "#FFEFC9" if on else "none"
        stroke = ("rgba(255,243,214,.55)" if dark else "rgba(36,16,63,.35)")
        cells.append(f'<svg viewBox="0 0 100 100" width="78" height="78"><circle cx="50" cy="50" r="42" fill="{fill}" stroke="{stroke}" stroke-width="4"/></svg>')
    return '<div class="mrow">' + "".join(cells) + '</div>'

CSS = """
@font-face{font-family:Fraunces;src:url(fonts/fraunces.woff2);font-weight:100 900}
@font-face{font-family:Fraunces;src:url(fonts/fraunces-italic.woff2);font-weight:100 900;font-style:italic}
@font-face{font-family:Figtree;src:url(fonts/figtree.woff2);font-weight:300 900}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:Wpx;height:Hpx;overflow:hidden}
.s{position:relative;width:Wpx;height:Hpx;overflow:hidden;font-family:Figtree,sans-serif;-webkit-font-smoothing:antialiased}
.night{background:radial-gradient(90% 55% at 70% 108%,rgba(186,112,168,.38) 0%,rgba(186,112,168,0) 70%),linear-gradient(180deg,#0E0620 0%,#1C0C3B 46%,#33175F 100%);color:#FFF3D6}
.dawn{background:radial-gradient(80% 50% at 85% -5%,rgba(255,255,255,.75) 0%,rgba(255,255,255,0) 70%),linear-gradient(170deg,#EDE3FA 0%,#F5E7F2 55%,#FBE2E8 100%);color:#24103F}
.photo{background:#0E0620;color:#FFF3D6}
.photo .bg{position:absolute;inset:0;background-size:cover;background-position:var(--pos,center)}
.photo .scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,6,32,.86) 0%,rgba(14,6,32,.55) 34%,rgba(14,6,32,0) 58%,rgba(14,6,32,0) 78%,rgba(14,6,32,.55) 100%)}
.stars{position:absolute;inset:0}
.grain{position:absolute;inset:0;background:url(img/grain0.png);opacity:.06;mix-blend-mode:overlay;pointer-events:none}
.pmoon{position:absolute;top:TOPpx;right:84px}
.dawn .pmoon{filter:drop-shadow(0 6px 14px rgba(36,16,63,.28))}
.wrap{position:absolute;left:96px;right:96px;top:TOPpx}
.wrap.low{top:auto;bottom:LOWpx}
.wrap.top .t{max-width:740px}
.t{font-family:Fraunces,serif;font-weight:420;font-size:TSpx;line-height:1.0;letter-spacing:-.028em;text-wrap:balance;max-width:880px;font-variation-settings:"opsz" 144}
.t.it{font-style:italic;font-weight:360}
.b{font-size:42px;line-height:1.42;margin-top:40px;max-width:820px;text-wrap:pretty;font-weight:450}
.night .b,.photo .b{color:rgba(255,243,214,.86)}
.dawn .b{color:#4F3C6B}
.b strong{font-weight:700}
.q{margin-top:44px;display:flex;flex-direction:column;gap:30px}
.q div{position:relative;font-family:Fraunces,serif;font-style:italic;font-weight:380;font-size:60px;line-height:1.12;letter-spacing:-.015em;padding-left:2px}
.q div::before{content:"\\201C";position:absolute;left:-56px;top:-8px;font-size:96px;color:#F4B6C8;font-style:normal}
.dawn .q div::before{color:#C8628A}
.mrow{display:flex;gap:16px;margin-top:56px;flex-wrap:wrap;max-width:880px}
.phone{position:absolute;width:PWpx;padding:12px;border-radius:72px;background:linear-gradient(145deg,#2A2238,#0B0712 45%,#1B1526);box-shadow:0 0 0 2px rgba(255,255,255,.06),0 50px 90px -30px rgba(14,6,32,.7)}
.phone img{display:block;width:100%;border-radius:60px}
.foot{position:absolute;left:96px;right:96px;bottom:FBpx;display:flex;justify-content:space-between;align-items:center}
.brand{display:flex;align-items:center;gap:12px;font-family:Fraunces,serif;font-weight:520;font-size:40px;letter-spacing:-.01em}
.brand img{width:40px;height:40px}
.dawn .brand img{filter:drop-shadow(0 0 1px rgba(36,16,63,.9)) drop-shadow(0 2px 4px rgba(36,16,63,.35))}
.withphone .b{max-width:520px}
.src{font-size:24px;opacity:.72;text-align:right;max-width:600px;line-height:1.3}
.cta{display:inline-flex;margin-top:52px;padding:24px 38px;border-radius:999px;font-weight:700;font-size:34px}
.night .cta,.photo .cta{background:#FFF3D6;color:#24103F}
.dawn .cta{background:#24103F;color:#FFF3D6}
.badges{display:flex;gap:20px;margin-top:48px}.badges img{height:88px}
"""

def slide(s, i, n, w, h, kind):
    theme = s.get("theme", "night")
    tall = h > 1500
    top = 250 if tall else 116
    fb = 400 if (tall and kind == "tt") else (300 if kind == "story" else 88)
    ts = s.get("size", 112 if not tall else 120)
    pw = s.get("phoneW", 500 if not tall else 560)
    low = fb + (140 if tall else 120)
    css = (CSS.replace("LOWpx", f"{low}px").replace("Wpx", f"{w}px").replace("Hpx", f"{h}px").replace("TOPpx", f"{top}px")
           .replace("TSpx", f"{ts}px").replace("FBpx", f"{fb}px").replace("PWpx", f"{pw}px"))
    parts = []
    if theme == "photo":
        img = (HERE / "img" / s["img"]).as_uri()
        parts.append(f'<div class="bg" style="background-image:url({img});--pos:{s.get("pos","center")}"></div><div class="scrim"></div>')
    if theme == "night":
        parts.append(stars(w, h))
    dark = theme != "dawn"
    if n > 1 and not s.get("noMoon"):
        parts.append(moon(i / (n - 1), dark=dark))
    inner = f'<div class="t{" it" if s.get("italic") else ""}">{esc(s.get("title"))}</div>'
    if s.get("body"):
        inner += f'<div class="b">{s["body"]}</div>'
    if s.get("quotes"):
        inner += '<div class="q">' + "".join(f"<div>{esc(q)}</div>" for q in s["quotes"]) + "</div>"
    if s.get("moons"):
        m = s["moons"]; inner += moon_row(m["total"], m["lit"], dark)
    if s.get("cta"):
        inner += f'<div><span class="cta">{esc(s["cta"])}</span></div>'
    if s.get("badges"):
        inner += f'<div class="badges"><img src="{(HERE/"img"/"app-store-badge.svg").as_uri()}"><img src="{(HERE/"img"/"google-play-badge.png").as_uri()}"></div>'
    anchor = s.get("anchor") or ("low" if theme in ("night", "dawn") and not s.get("phone") else "top")
    parts.append(f'<div class="wrap {anchor}{" withphone" if s.get("phone") else ""}">{inner}</div>')
    mark = (HERE / "img" / "mark-moon.svg").as_uri()
    src_txt = esc(s.get("source", ""))
    parts.append(f'<div class="foot"><div class="brand"><img src="{mark}">Clari</div><div class="src">{src_txt}</div></div>')
    if s.get("phone"):
        src = (HERE / "img" / s["phone"]).as_uri()
        y = s.get("phoneY", 600 if not tall else 900)
        x = s.get("phoneX", w - pw - 70)
        rot = s.get("phoneRot", -4)
        parts.append(f'<div class="phone" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"><img src="{src}"></div>')
    parts.append('<div class="grain"></div>')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="s {theme}">{"".join(parts)}</div></body></html>'

def main():
    content = json.loads(pathlib.Path(sys.argv[1]).read_text())
    out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    kinds = content.get("sizes", ["ig", "tt"])
    slides = content["slides"]; n = len(slides)
    tmp = HERE / "_s.html"
    with sync_playwright() as p:
        b = p.chromium.launch()
        for kind in kinds:
            w, h = SIZES[kind]
            pg = b.new_page(viewport={"width": w, "height": h})
            for i, s in enumerate(slides):
                ov = s.get(kind, {})
                tmp.write_text(slide({**s, **ov}, i, n, w, h, kind))
                pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
                pg.screenshot(path=str(out / f"{content['slug']}-{kind}-{i + 1:02d}.jpg"), type="jpeg", quality=93)
        b.close()
    tmp.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
