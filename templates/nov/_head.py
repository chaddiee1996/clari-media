"""Clari November 2026 feed + stories renderer.

python3 nov.py OUT [post ...]      render posts (default all)
Every post is a function returning a list of slide HTML bodies for a size.
Sizes: ig 1080x1350 (feed 4:5), tt 1080x1920 (TikTok photo), st 1080x1920 (story).

After rendering, every page is checked in the browser for:
  - any text box overflowing its container (clipped text)
  - any text outside the canvas or inside the platform's UI danger zones
A failing page is reported and the script exits non-zero.
"""
import html, json, math, pathlib, re, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SIZES = {"ig": (1080, 1350), "tt": (1080, 1920), "st": (1080, 1920)}
# Areas covered by app UI. (left, top, right, bottom) margins in px that text must avoid.
SAFE = {"ig": (60, 60, 60, 60), "tt": (60, 150, 150, 420), "st": (60, 230, 60, 330)}

def U(p):
    return (HERE / p).as_uri()

def icon(name, size=64, color="currentColor", cls=""):
    svg = (HERE / "icons" / f"{name}-duotone.svg").read_text()
    svg = svg.replace("<svg ", f'<svg class="ic {cls}" width="{size}" height="{size}" style="color:{color}" ', 1)
    return svg

def e(t):
    return html.escape(t or "").replace("|", "<br>")

FONTS = f"""
@font-face{{font-family:F;src:url({U('fonts/fraunces-full.woff2')});font-weight:100 900}}
@font-face{{font-family:F;src:url({U('fonts/fraunces-full-italic.woff2')});font-weight:100 900;font-style:italic}}
@font-face{{font-family:S;src:url({U('fonts/figtree.woff2')});font-weight:300 900}}
@font-face{{font-family:H;src:url({U('fonts/caveat.woff2')})}}
@font-face{{font-family:IS;src:url({U('fonts/instrument-serif.woff2')})}}
@font-face{{font-family:IS;src:url({U('fonts/instrument-serif-italic.woff2')});font-style:italic}}
@font-face{{font-family:IN;src:url({U('fonts/instrument-sans.woff2')});font-weight:400 700}}
@font-face{{font-family:M;src:url({U('fonts/dm-mono-400.woff2')});font-weight:400}}
@font-face{{font-family:M;src:url({U('fonts/dm-mono-500.woff2')});font-weight:500}}
"""

BASE = """
:root{--plum:#24103F;--plum2:#3A1C63;--violet:#6B3FA0;--lilac:#D9C8F2;--lilac2:#EEE6FA;--blush:#F3B9C9;
--rose:#C8628A;--cream:#FBF5EA;--paper:#FFFBF3;--butter:#FFE58A;--ink:#1E1233;--moon:#FFF3D6}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:Wpx;height:Hpx;overflow:hidden;background:#000}
.c{position:relative;width:Wpx;height:Hpx;overflow:hidden;font-family:S,sans-serif;color:var(--ink);
  -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;font-kerning:normal}
.F{font-family:F,serif;font-variation-settings:"opsz" 144,"SOFT" 50,"WONK" 0;letter-spacing:-.022em;line-height:1.02;text-wrap:balance}
.grain{position:absolute;inset:0;pointer-events:none;background:url(GRAIN);background-size:540px 960px;opacity:.07;mix-blend-mode:multiply}
.grain.l{mix-blend-mode:overlay;opacity:.09}
.brand{position:absolute;display:flex;align-items:center;gap:12px;font-family:F,serif;font-variation-settings:"opsz" 72,"SOFT" 50;font-weight:560;font-size:38px;letter-spacing:-.01em}
.brand img{width:38px;height:38px}
.src{font-family:S;font-size:24px;font-weight:550;letter-spacing:.005em;opacity:.7}
.ic{display:block;flex:none}
"""

def page(w, h, css, body, kind):
    base = BASE.replace("Wpx", f"{w}px").replace("Hpx", f"{h}px").replace("GRAIN", U("img/grain0.png"))
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{base}{css}</style></head>'
            f'<body data-kind="{kind}"><div class="c">{body}</div></body></html>')

def brand(x, y, dark=False, anchor="left"):
    mark = U("img/mark-moon.svg")
    col = "#FFF3D6" if dark else "var(--plum)"
    pos = f"left:{x}px" if anchor == "left" else f"right:{x}px"
    filt = "" if dark else ' style="filter:drop-shadow(0 0 1px rgba(36,16,63,.9))"'
    return f'<div class="brand" style="{pos};top:{y}px;color:{col}"><img src="{mark}"{filt}>Clari</div>'

