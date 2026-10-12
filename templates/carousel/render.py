"""Clari carousel renderer.

Usage: python3 render.py content.json OUTDIR
content.json: {"slug": "...", "slides": [{"kind": "cover"|"item"|"end", ...}]}
Renders every slide at 1080x1350 (Instagram 4:5) and 1080x1920 (TikTok 9:16).
The sky moves from deep night on the first slide to dawn on the last,
and the moon in the corner fills as you swipe (the app's own motif).
"""
import json, math, sys, pathlib, html
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
FONTS = HERE / "fonts"

NIGHT = [(10, 4, 24), (23, 10, 51), (42, 18, 82), (62, 28, 110)]
DAWN = [(30, 12, 58), (78, 36, 128), (168, 92, 160), (246, 196, 200)]


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky(t):
    stops = [mix(NIGHT[i], DAWN[i], t) for i in range(4)]
    pos = [0, 38, 72, 100]
    return "linear-gradient(180deg," + ",".join(
        f"rgb{c} {p}%" for c, p in zip(stops, pos)) + ")"


def rnd(i):
    x = math.sin(i * 127.1 + 311.7) * 43758.5453
    return x - math.floor(x)


def stars(w, h, t, seed):
    n = int(70 * (1 - t) + 12)
    out = []
    for i in range(n):
        x = rnd(i + seed) * w
        y = rnd(i + 500 + seed) * h * 0.26
        r = 0.9 + rnd(i + 900) * 1.8
        o = (0.25 + rnd(i + 41) * 0.6) * (1 - 0.7 * t)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#FFF8EA" opacity="{o:.2f}"/>')
    for i in range(5):
        x = 80 + rnd(i + 1200 + seed) * (w - 160)
        y = 120 + rnd(i + 1300 + seed) * h * 0.14
        s = 0.9 + rnd(i + 1400) * 0.8
        out.append(f'<path d="M0 -9 Q0 0 9 0 Q0 0 0 9 Q0 0 -9 0 Q0 0 0 -9Z" fill="#FFF3D6" '
                   f'opacity="{0.8 * (1 - 0.6 * t):.2f}" transform="translate({x:.0f} {y:.0f}) scale({s:.2f})"/>')
    return f'<svg class="stars" width="{w}" height="{h}">{"".join(out)}</svg>'


def moon(fill):
    """Moon whose lit part grows with fill (0..1)."""
    # shadow circle slides off to the right as fill increases
    off = 36 + fill * 70
    return f'''<svg class="moon" viewBox="0 0 100 100" width="120" height="120">
<defs><radialGradient id="mg" cx="0.35" cy="0.3" r="0.9"><stop offset="0" stop-color="#FFFBEE"/>
<stop offset="0.6" stop-color="#FFEFC9"/><stop offset="1" stop-color="#F2C9A0"/></radialGradient>
<mask id="mm"><rect width="100" height="100" fill="#fff"/><circle cx="{50 + off:.1f}" cy="44" r="40" fill="#000"/></mask></defs>
<circle cx="50" cy="50" r="40" fill="rgba(255,243,214,0.10)"/>
<circle cx="50" cy="50" r="40" fill="url(#mg)" mask="url(#mm)"/></svg>'''


def small_moon(level):
    """App-style severity moon: fills from the left as the symptom gets stronger."""
    w = 72
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="rgba(255,243,214,.16)" stroke="rgba(255,243,214,.5)" stroke-width="3"/>'
            f'<clipPath id="c"><rect x="0" y="0" width="{level*100:.0f}" height="100"/></clipPath>'
            f'<circle cx="50" cy="50" r="44" fill="#FFEFC9" clip-path="url(#c)"/></svg>')


CSS = """
@font-face{font-family:Fraunces;src:url(fonts/fraunces.woff2);font-weight:100 900}
@font-face{font-family:Fraunces;src:url(fonts/fraunces-italic.woff2);font-weight:100 900;font-style:italic}
@font-face{font-family:Figtree;src:url(fonts/figtree.woff2);font-weight:300 900}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:WPX;height:HPX;overflow:hidden;background:#0A0418}
.s{position:relative;width:WPX;height:HPX;overflow:hidden;color:#fff;font-family:Figtree,sans-serif}
.stars{position:absolute;inset:0}
.glow{position:absolute;inset:0;background:radial-gradient(70% 40% at 50% 100%,rgba(249,201,216,GLOW) 0%,rgba(249,201,216,0) 70%)}
.vig{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 45%,rgba(0,0,0,0) 55%,rgba(5,2,12,.5) 100%)}
.grain{position:absolute;inset:0;background:url(fonts/grain0.png);opacity:.07;mix-blend-mode:overlay}
.moon{position:absolute;top:PADpx;right:PADpx}
.wrap{position:absolute;left:96px;right:96px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}
.kicker{font-weight:700;letter-spacing:.22em;font-size:26px;color:#F9C9D8;text-transform:uppercase}
.num{font-family:Fraunces;font-style:italic;font-weight:300;font-size:150px;line-height:1;color:#F9C9D8;opacity:.9}
.title{font-family:Fraunces;font-weight:500;font-size:TITLEpx;line-height:1.02;letter-spacing:-.02em;margin-top:28px;text-wrap:balance}
.title em{font-style:italic;font-weight:400;color:#FFE3EC}
.body{font-size:44px;line-height:1.35;color:rgba(255,255,255,.86);margin-top:36px;max-width:820px;text-wrap:pretty}
.cta{display:inline-block;margin-top:48px;padding:22px 34px;border-radius:999px;background:#FFF3D6;color:#2A1252;font-weight:700;font-size:34px}
.foot{position:absolute;left:96px;right:FOOTRpx;bottom:FOOTBpx;display:flex;justify-content:space-between;align-items:flex-end;font-size:26px;color:rgba(255,255,255,.7)}
.brand{font-family:Fraunces;font-weight:500;font-size:40px;color:#fff;letter-spacing:-.01em}
.dots{display:flex;gap:10px}.dots i{width:10px;height:10px;border-radius:5px;background:rgba(255,255,255,.3)}.dots i.on{background:#F9C9D8;width:30px}
.card{margin-top:64px;display:flex;align-items:center;gap:28px;padding:26px 32px;border-radius:36px;background:rgba(255,255,255,.10);border:1.5px solid rgba(255,255,255,.18);backdrop-filter:blur(8px);max-width:760px}
.tile{width:92px;height:92px;border-radius:26px;background:rgba(195,168,234,.22);display:flex;align-items:center;justify-content:center;color:#E4D4FF;flex:none}
.tile svg{width:58px;height:58px}
.ctext{flex:1}.clabel{font-size:22px;font-weight:700;letter-spacing:.18em;color:#F9C9D8}
.cname{font-size:40px;font-weight:600;margin-top:6px}
.cmoon{flex:none}
.swipe{margin-top:60px;font-size:30px;color:rgba(255,255,255,.75);letter-spacing:.04em}
"""


def slide_html(s, i, n, w, h):
    t = i / max(1, n - 1)
    pad = 84 if h > 1500 else 64
    title_px = s.get("titleSize", 112 if s["kind"] == "item" else 120)
    css = (CSS.replace("WPX", f"{w}px").replace("HPX", f"{h}px").replace("PADpx", f"{pad}px")
           .replace("TITLEpx", f"{title_px}px").replace("FOOTBpx", f"{420 if h > 1500 else pad}px").replace("FOOTRpx", f"{180 if h > 1500 else 96}px").replace("GLOW", f"{0.08 + 0.32 * t:.2f}"))
    e = lambda k: s.get(k, "")
    dots = "".join(f'<i class="{"on" if j == i else ""}"></i>' for j in range(n))
    if s["kind"] == "cover":
        inner = (f'<div class="kicker">{e("kicker")}</div><div class="title">{e("title")}</div>'
                 f'<div class="body">{e("body")}</div><div class="swipe">Swipe &rarr;</div>')
    elif s["kind"] == "item":
        card = ""
        if s.get("app"):
            a = s["app"]
            icon = (HERE / "icons" / f"{a['icon']}.svg").read_text()
            card = (f'<div class="card"><div class="tile">{icon}</div><div class="ctext">'
                    f'<div class="clabel">LOG IT IN CLARI</div><div class="cname">{a["name"]}</div></div>'
                    f'<div class="cmoon">{small_moon(a.get("level", 0.5))}</div></div>')
        inner = (f'<div class="num">{e("num")}</div><div class="title">{e("title")}</div>'
                 f'<div class="body">{e("body")}</div>{card}')
    else:
        inner = (f'<div class="title">{e("title")}</div><div class="body">{e("body")}</div>'
                 + (f'<div><span class="cta">{e("cta")}</span></div>' if s.get("cta") else ""))
    foot_left = '<span class="brand">Clari</span>'
    foot_mid = f'<span>{e("source")}</span>' if s.get("source") else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="s" style="background:{sky(t)}">{stars(w, h, t, 7)}<div class="glow"></div><div class="vig"></div>
{moon(t)}<div class="wrap">{inner}</div>
<div class="foot">{foot_left}{foot_mid}<div class="dots">{dots}</div></div><div class="grain"></div></div></body></html>"""


def main():
    content = json.loads(pathlib.Path(sys.argv[1]).read_text())
    out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    slides = content["slides"]; n = len(slides)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for (w, h, tag) in [(1080, 1350, "ig"), (1080, 1920, "tt")]:
            pg = b.new_page(viewport={"width": w, "height": h})
            for i, s in enumerate(slides):
                f = HERE / f"_slide.html"
                f.write_text(slide_html(s, i, n, w, h))
                pg.goto(f.as_uri()); pg.wait_for_timeout(250)
                pg.evaluate("document.fonts.ready")
                pg.screenshot(path=str(out / f"{content['slug']}-{tag}-{i + 1:02d}.jpg"), type="jpeg", quality=92)
        b.close()
    (HERE / "_slide.html").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
