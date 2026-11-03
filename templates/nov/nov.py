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

# ---------------------------------------------------------------------------
# Layout helpers shared by feed posts
# ---------------------------------------------------------------------------
def frame(kind):
    """Returns (w, h, tall, L, R, top, by, sy): margins, content top, brand y, source y."""
    w, h = SIZES[kind]
    tall = h > 1500
    L = 84
    R = 150 if kind == "tt" else 84
    top = 260 if tall else 110
    by = h - (520 if kind == "tt" else 112)
    return w, h, tall, L, R, top, by, by + 8

def foot(kind, dark=False, right=None, mono=False, color=None):
    w, h, tall, L, R, top, by, sy = frame(kind)
    out = brand(L, by, dark)
    if right:
        col = color or ("var(--moon)" if dark else "var(--plum)")
        fam = "font-family:M;font-size:26px;" if mono else ""
        out += f'<div class="src" style="position:absolute;right:{R}px;top:{sy}px;color:{col};{fam}">{e(right)}</div>'
    return out

def mid(kind, inner, L=None, R=None, pad=40):
    w, h, tall, L0, R0, top, by, sy = frame(kind)
    L = L0 if L is None else L; R = R0 if R is None else R
    return (f'<div style="position:absolute;left:{L}px;right:{R}px;top:{top}px;bottom:{h - by + pad}px;'
            f'display:flex;flex-direction:column;justify-content:center">{inner}</div>')

def blossom(x, y, width, flip=False, rot=0, op=1):
    t = f"scaleX(-1) rotate({rot}deg)" if flip else f"rotate({rot}deg)"
    return f'<img class="deco" src="{U("img/blossom-branch.svg")}" style="position:absolute;left:{x}px;top:{y}px;width:{width}px;transform:{t};opacity:{op};pointer-events:none">'

def phone(src, width, style=""):
    return (f'<div style="position:absolute;width:{width}px;padding:{width*0.026:.0f}px;border-radius:{width*0.14:.0f}px;'
            f'background:linear-gradient(145deg,#3a3050,#0b0712 45%,#221a33);box-shadow:0 0 0 2px rgba(255,255,255,.05),0 60px 100px -40px rgba(20,8,40,.75);{style}">'
            f'<img src="{U("img/" + src)}" style="display:block;width:100%;border-radius:{width*0.118:.0f}px"></div>')

# ---------------------------------------------------------------------------
# 11 Nov. Things women still get told (message thread carousel)
# ---------------------------------------------------------------------------
THREAD = [
    ("You're too young for that.",
     "Menopause usually happens between 45 and 55, and it can happen earlier. Perimenopause, the change before it, often starts sooner.",
     "nhs.uk"),
    ("It's probably just stress.",
     "Maybe. But low mood, anxiety and problems with memory are all on the NHS list of perimenopause symptoms.",
     "nhs.uk"),
    ("Isn't it just hot flushes?",
     "The NHS list also includes joint pain, headaches, itchy skin, heart palpitations and trouble sleeping.",
     "nhs.uk"),
    ("You'd need a blood test to know.",
     "Not usually. For women over 45 with symptoms, NICE says it can be diagnosed without one.",
     "NICE guideline NG23"),
    ("It'll all be over in a year.",
     "Symptoms usually last 7 to 9 years, sometimes longer, and they can change along the way.",
     "nhs.uk"),
]

def thread(kind):
    w, h, tall, L, R, top, by, sy = frame(kind)
    css = """
.c{background:radial-gradient(110% 60% at 100% 0%,#EADFFA 0%,rgba(234,223,250,0) 62%),radial-gradient(90% 50% at 0% 100%,#F6E3EC 0%,rgba(246,227,236,0) 70%),#F6F2FB}
.col{position:absolute;display:flex;flex-direction:column}
.in,.out{position:relative;border-radius:52px;letter-spacing:-.014em}
.in{align-self:flex-start;max-width:820px;background:#fff;color:#2A1D40;padding:40px 50px 44px;font-size:68px;line-height:1.12;font-weight:650;
  border-bottom-left-radius:16px;box-shadow:0 1px 0 rgba(36,16,63,.05),0 24px 50px -26px rgba(36,16,63,.3)}
.out{align-self:flex-end;max-width:840px;background:linear-gradient(160deg,#4E2686 0%,#2C1350 100%);color:#FFF6E4;padding:44px 52px 48px;
  font-size:50px;line-height:1.3;font-weight:500;border-bottom-right-radius:16px;box-shadow:0 40px 70px -34px rgba(44,19,80,.65)}
.who{font-family:M;font-size:26px;color:#8B7AA6;margin:0 0 18px 8px;letter-spacing:.02em}
.who.r{align-self:flex-end;margin:20px 8px 0 0}
.dots{display:flex;gap:14px;padding:8px 6px}
.dots i{width:24px;height:24px;border-radius:50%;background:#B9A9D3;display:block}
.dots i:nth-child(2){opacity:.6}.dots i:nth-child(3){opacity:.3}
.h{font-size:132px;font-weight:420;color:var(--plum)}
.h em{font-style:italic;font-weight:360;color:var(--violet)}
.swipe{font-family:H;font-size:64px;color:var(--rose);display:flex;align-items:center;gap:16px}
.q{position:absolute;font-family:F;font-style:italic;font-weight:300;font-size:620px;line-height:1;color:#E6DBF6;pointer-events:none}
"""
    n = len(THREAD) + 2
    slides = []
    body = f"""
{blossom(w - 600, 30 if not tall else 150, 640, flip=False, rot=4, op=.95)}
<div class="col" style="left:{L}px;right:{R}px;top:{top + (330 if tall else 250)}px">
  <div class="h F">Things women still get told about <em>perimenopause</em></div>
  <div style="height:{80 if tall else 60}px"></div>
  <div class="in" style="padding:34px 42px"><div class="dots"><i></i><i></i><i></i></div></div>
  <div style="height:{64 if tall else 52}px"></div>
  <div class="swipe">And what the NHS actually says {icon('hand-swipe-left', 66, 'var(--rose)')}</div>
</div>
{foot(kind)}<div class="grain"></div>"""
    slides.append(body)
    for i, (said, reply, src) in enumerate(THREAD):
        body = f"""
{mid(kind, f"""<div style="display:flex;flex-direction:column">
  <div class="who">What women hear</div>
  <div class="in">{e(said)}</div>
  <div style="height:{90 if tall else 64}px"></div>
  <div class="out">{e(reply)}</div>
  <div class="who r">Source: {e(src)}</div></div>""")}
{foot(kind, right=f"{i + 2} / {n}", mono=True, color="#8B7AA6")}<div class="grain"></div>"""
        slides.append(body)
    body = f"""
{blossom(w - 560, 40 if not tall else 120, 600, rot=6, op=.9)}
<div class="col" style="left:{L}px;right:{R}px;top:{top + (120 if tall else 40)}px">
  {icon('paper-plane-tilt', 170, 'var(--violet)')}
  <div style="height:56px"></div>
  <div class="h F" style="font-size:{116 if tall else 112}px">Send this to someone who's been told it's <em>nothing.</em></div>
  <div style="height:44px"></div>
  <div style="font-size:46px;line-height:1.38;color:#4F3C6B;font-weight:460;max-width:860px">Then start writing down what you notice. Clari makes it a minute a day.</div>
</div>
{foot(kind, right="Free on the App Store and Google Play")}<div class="grain"></div>"""
    slides.append(body)
    return css, slides

# ---------------------------------------------------------------------------
# 14 Nov. Age ruler poster (single image)
# ---------------------------------------------------------------------------
def ruler(kind):
    w, h, tall, L, R, top, by, sy = frame(kind)
    css = """
.c{background:radial-gradient(90% 60% at 0% 100%,#F8D0DB 0%,rgba(248,208,219,0) 70%),radial-gradient(70% 50% at 100% 0%,#EFA8BC 0%,rgba(239,168,188,0) 70%),#F3B6C6;color:var(--plum)}
.t{position:absolute;font-size:120px;font-weight:440}
.t em{font-style:italic;font-weight:380}
.rule{position:absolute;height:300px}
.axis{position:absolute;left:0;right:0;top:186px;height:5px;background:var(--plum);border-radius:3px}
.tick{position:absolute;top:166px;width:4px;height:46px;background:var(--plum);transform:translateX(-50%);border-radius:2px}
.tick.s{top:178px;height:22px;opacity:.5;width:3px}
.lab{position:absolute;top:232px;font-family:M;font-size:36px;font-weight:500;transform:translateX(-50%)}
.band{position:absolute;top:24px;height:126px;border-radius:30px;background:var(--plum);box-shadow:0 30px 60px -30px rgba(36,16,63,.7);
  display:flex;align-items:center;justify-content:center;color:#FFE4EC;font-family:F;font-variation-settings:"opsz" 144,"SOFT" 50;font-size:62px;font-weight:500;letter-spacing:-.02em}
.pre{position:absolute;top:24px;height:126px;border-radius:30px 0 0 30px;
  background:repeating-linear-gradient(135deg,rgba(36,16,63,.3) 0 4px,rgba(36,16,63,0) 4px 20px);
  -webkit-mask:linear-gradient(90deg,transparent,#000 75%);mask:linear-gradient(90deg,transparent,#000 75%)}
.note{position:absolute;font-family:H;font-size:56px;line-height:1.02;color:var(--plum);white-space:nowrap}
.b{position:absolute;font-size:46px;line-height:1.38;font-weight:480;color:#46204E}
"""
    lo, hi = 35, 61
    span = w - L - R
    X = lambda a: (a - lo) / (hi - lo) * span
    ticks = "".join(f'<div class="tick{"" if a % 5 == 0 else " s"}" style="left:{X(a):.1f}px"></div>' for a in range(lo + 1, hi))
    labs = "".join(f'<div class="lab" style="left:{X(a):.1f}px">{a}</div>' for a in (40, 45, 50, 55, 60))
    ry = top + (560 if tall else 640)
    arrow = '<svg width="90" height="70" viewBox="0 0 90 70" fill="none" stroke="#24103F" stroke-width="5" stroke-linecap="round"><path d="M6 10 C 40 6, 70 22, 78 58"/><path d="M62 48 L78 62 L86 40"/></svg>'
    body = f"""
<div class="t F" style="left:{L}px;right:{R}px;top:{top}px">Menopause usually happens between <em>45 and 55.</em></div>
<div class="rule" style="left:{L}px;right:{R}px;top:{ry}px">
  <div class="note" style="left:0;top:-100px;display:flex;align-items:flex-end;gap:6px">perimenopause often starts earlier {arrow}</div>
  <div class="pre" style="left:{X(37):.1f}px;width:{X(45) - X(37):.1f}px"></div>
  <div class="band" style="left:{X(45):.1f}px;width:{X(55) - X(45):.1f}px">age 45 to 55</div>
  <div class="axis"></div>{ticks}{labs}
</div>
<div class="b" style="left:{L}px;right:{R}px;top:{ry + (330 if tall else 320)}px">And it can happen earlier. If your body feels different, start noting what's changing.</div>
{foot(kind, right="Source: nhs.uk")}<div class="grain"></div>"""
    return css, [body]

# ---------------------------------------------------------------------------
# 17 Nov. Self Care Week: notes for tonight (sticky notes)
# ---------------------------------------------------------------------------
NOTES = [
    ("#FFE27A", -3.0, "Keep the|bedroom cool.|Light layers|to bed.", "A lighter duvet and breathable nightwear can help."),
    ("#F9C4D3", 2.4, "Cool down fast.|Cool shower, a fan,|a cold drink.", "Keep a glass of water by the bed for the 3am wake up."),
    ("#C9EBD6", -1.8, "Notice what|sets it off.", "The NHS names spicy food, caffeine, hot drinks, smoking and alcohol. Yours could be different."),
    ("#DCCDF6", 1.9, "Move most days.|Find ways to|unwind.", "Regular exercise and lower stress can help. The NHS says CBT can help with hot flushes too."),
    ("#FFE27A", -2.4, "Still struggling?|Talk to your GP.", "About what might help, including treatments that could suit you."),
]

def notes(kind):
    w, h, tall, L, R, top, by, sy = frame(kind)
    css = """
.c{background:radial-gradient(80% 50% at 85% 5%,#3E2670 0%,rgba(62,38,112,0) 70%),radial-gradient(70% 60% at 0% 100%,#2C1754 0%,rgba(44,23,84,0) 70%),#170B2C;color:var(--moon)}
.note{position:absolute;display:flex;align-items:center;padding:0 70px 20px;border-radius:4px 4px 30px 6px;
  box-shadow:0 2px 0 rgba(0,0,0,.05),0 60px 90px -36px rgba(0,0,0,.7),inset 0 -50px 70px -50px rgba(110,70,0,.2)}
.note::after{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(165deg,rgba(255,255,255,.4),rgba(255,255,255,0) 38%);pointer-events:none}
.tape{position:absolute;top:-34px;left:50%;width:240px;height:68px;margin-left:-120px;background:rgba(255,255,255,.45);box-shadow:0 2px 6px rgba(0,0,0,.12)}
.hw{font-family:H;font-size:112px;line-height:1.0;color:#271A3D}
.sub{position:absolute;font-size:46px;line-height:1.38;font-weight:470;color:rgba(255,243,214,.9)}
.h1{position:absolute;font-size:124px;color:var(--moon);font-weight:420}
.h1 em{font-style:italic;font-weight:360;color:#F7C6D3}
.moon{position:absolute;width:170px;height:170px;border-radius:50%;box-shadow:inset -38px 12px 0 0 #FFEFC9;transform:rotate(-20deg);filter:drop-shadow(0 0 30px rgba(255,239,201,.35))}
.star{position:absolute;width:6px;height:6px;border-radius:50%;background:#FFF3D6}
"""
    stars = "".join(f'<div class="star" style="left:{(i*263)%w}px;top:{40+(i*97)%(420 if tall else 300)}px;opacity:{.25+(i%4)*.15:.2f};transform:scale({.6+(i%3)*.4:.1f})"></div>' for i in range(22))
    slides = []
    nw = w - L - R - 60
    body = f"""{stars}
<div class="moon" style="right:{R + 10}px;top:{top}px"></div>
<div class="h1 F" style="left:{L}px;right:{R}px;top:{top + 230}px">Night sweats? <em>Notes for tonight.</em></div>
<div class="note" style="left:{L + 60}px;top:{top + (640 if tall else 640)}px;width:{nw - 120}px;height:{360 if not tall else 400}px;background:#F9C4D3;transform:rotate(-3deg)">
  <div class="tape" style="transform:rotate(4deg)"></div><div class="hw" style="font-size:86px">Five small things the NHS suggests</div></div>
{foot(kind, dark=True, right="For Self Care Week, 16 to 22 November")}<div class="grain l"></div>"""
    slides.append(body)
    for i, (col, rot, hw, sub) in enumerate(NOTES):
        side = nw
        ny = top + (40 if tall else 10)
        body = f"""{stars}
<div class="note" style="left:{L + 30}px;top:{ny}px;width:{side}px;height:{side - (0 if tall else 120)}px;background:{col};transform:rotate({rot}deg)">
  <div class="tape" style="transform:rotate({-rot * 1.5:.1f}deg)"></div>
  <div class="hw">{e(hw)}</div>
</div>
<div class="sub" style="left:{L}px;right:{R}px;top:{ny + side - (0 if tall else 120) + (90 if tall else 60)}px">{e(sub)}</div>
{foot(kind, dark=True, right="Source: nhs.uk")}<div class="grain l"></div>"""
        slides.append(body)
    pw = 420
    body = f"""{stars}
<div class="h1 F" style="left:{L}px;right:{R}px;top:{top}px;font-size:{116 if tall else 104}px">Log the nights. <em>Spot your pattern.</em></div>
<div class="sub" style="left:{L}px;top:{top + (300 if tall else 270)}px;width:{480 if not tall else 800}px">Clari keeps a private record of your symptoms and triggers, ready for your GP.</div>
{phone('app-log.png', 360 if tall else pw, f"right:{R + (80 if tall else 0)}px;top:{top + (660 if tall else 330)}px;transform:rotate(4deg)")}
{foot(kind, dark=True)}
<div class="src" style="position:absolute;left:{L}px;top:{(top + 560) if tall else (by - 64)}px;color:var(--moon)">Free on the App Store and Google Play</div>
<div class="grain l"></div>"""
    slides.append(body)
    return css, slides

# ---------------------------------------------------------------------------
# 23 Nov. GP appointment checklist (card carousel)
# ---------------------------------------------------------------------------
CHECK = [
    ("In the weeks before", [
        "Log your symptoms daily, and how strong they feel",
        "Note any changes to your periods",
        "Jot down anything that seems to set things off",
    ], "Weeks of notes say more than memory on the day."),
    ("When you book", [
        "Ask reception which GP is best to see about menopause",
        "Ask for a longer appointment if you can",
    ], "Tip from Nuffield Health"),
    ("In the room", [
        "Say it plainly: “I think this could be perimenopause.”",
        "Share your summary, rather than recalling from memory",
        "Ask: “What are my options?”",
    ], "Tip from Nuffield Health"),
    ("Good to know", [
        "Over 45 with symptoms? NICE says it can be diagnosed without a blood test",
        "Between 40 and 45, a blood test may be considered",
    ], "Source: NICE guideline NG23"),
]

def checklist(kind):
    w, h, tall, L, R, top, by, sy = frame(kind)
    css = """
.c{background:radial-gradient(90% 60% at 0% 0%,#ECE2FC 0%,rgba(236,226,252,0) 70%),linear-gradient(160deg,#D5C1F2 0%,#E4D0EE 55%,#F2D3E0 100%)}
.card{position:absolute;background:var(--paper);border-radius:44px;padding:84px 72px 70px;overflow:hidden;
  box-shadow:0 2px 0 rgba(36,16,63,.04),0 70px 110px -60px rgba(60,30,110,.6)}
.card::before{content:"";position:absolute;left:0;right:0;top:0;height:16px;background:linear-gradient(90deg,#6B3FA0,#C8628A)}
.ct{font-family:IS;font-size:104px;line-height:.98;color:var(--plum);letter-spacing:-.012em}
.ct em{font-style:italic}
.row{display:flex;gap:32px;align-items:flex-start;padding:34px 0;border-top:2px solid #EFE7F6}
.lbl+.row{border-top:0}
.box{flex:none;width:58px;height:58px;border-radius:16px;border:5px solid var(--violet);margin-top:2px}
.rt{font-family:IN;font-size:48px;line-height:1.24;color:#2A1D40;font-weight:500;letter-spacing:-.008em}
.num{flex:none;width:58px;font-family:IS;font-style:italic;font-size:64px;line-height:.9;color:var(--violet)}
.ft{font-family:IN;font-size:30px;color:#7A6894;font-weight:500;margin-top:20px}
.lbl{font-family:IS;font-style:italic;font-size:80px;line-height:1;color:var(--violet);margin-bottom:24px}
.shot{position:absolute;font-family:H;font-size:68px;color:var(--plum);line-height:1;display:flex;gap:16px;align-items:flex-start}
"""
    n = len(CHECK) + 2
    slides = []
    arrow = '<svg width="130" height="120" viewBox="0 0 130 120" fill="none" stroke="#24103F" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14 C 60 10, 104 34, 108 96"/><path d="M88 80 L108 100 L124 74"/></svg>'
    rows = "".join(f'<div class="row" style="align-items:center"><div class="num">{k + 1}</div><div class="rt">{e(t)}</div></div>' for k, (t, _, _) in enumerate(CHECK))
    body = f"""
<div class="card" style="left:{L - 12}px;right:{R - 12}px;top:{top}px">
  <div class="ct">Before your <em>GP appointment</em></div>
  <div style="height:36px"></div>
  <div class="lbl" style="display:none"></div>{rows}
</div>
<div class="shot" style="left:{L + 10}px;top:{top + (1020 if tall else 900)}px">Screenshot this for later {arrow}</div>
{foot(kind)}<div class="grain"></div>"""
    slides.append(body)
    for i, (lbl, items, ft) in enumerate(CHECK):
        rows = "".join(f'<div class="row"><div class="box"></div><div class="rt">{e(t)}</div></div>' for t in items)
        card = f'<div class="card" style="position:relative"><div class="lbl">{e(lbl)}</div>{rows}<div class="ft">{e(ft)}</div></div>'
        body = f"""
{mid(kind, card, L - 12, R - 12)}
{foot(kind, right=f"{i + 2} / {n}", mono=True)}<div class="grain"></div>"""
        slides.append(body)
    pw = 540 if tall else 430
    body = f"""
<div class="ct" style="position:absolute;left:{L}px;right:{R}px;top:{top}px;font-size:{112 if tall else 100}px">The easy way to <em>bring the notes</em></div>
<div class="rt" style="position:absolute;left:{L}px;top:{top + (250 if tall else 230)}px;width:{440 if not tall else 820}px;font-size:42px;color:#4F3C6B">Clari turns a minute a day into a summary you can share with your GP.</div>
{phone('app-summary.png', 350 if tall else pw, (f"left:{(w - 350)//2 - 30}px;top:{top + 500}px;transform:rotate(-3deg)" if tall else f"right:{R}px;top:{top + 240}px;transform:rotate(3deg)"))}
{foot(kind)}
<div class="src" style="position:absolute;left:{L}px;top:{(top + 400) if tall else (by - 64)}px;color:var(--plum)">Free on the App Store and Google Play</div>
<div class="grain"></div>"""
    slides.append(body)
    return css, slides

# ---------------------------------------------------------------------------
# 26 Nov. Which one did nobody warn you about? (grid, single)
# ---------------------------------------------------------------------------
GRID = [
    ("flame", "Hot flushes"), ("drop", "Night sweats"), ("brain", "Brain fog"), ("person-simple-walk", "Joint pain"),
    ("heartbeat", "Palpitations"), ("first-aid", "Headaches"), ("feather", "Itchy skin"), ("bed", "Poor sleep"),
    ("smiley-sad", "Low mood"), ("wave-sine", "Anxiety"), ("scissors", "Thinning hair"), ("scales", "Weight gain"),
    ("toilet", "Needing the loo more"), ("heart", "Lower sex drive"), ("calendar-dots", "Period changes"), ("drop-half", "Vaginal dryness"),
]

def grid(kind):
    w, h, tall, L, R, top, by, sy = frame(kind)
    css = """
.c{background:radial-gradient(80% 50% at 100% 0%,#F6E6D6 0%,rgba(246,230,214,0) 70%),var(--cream)}
.t{position:absolute;font-size:100px;font-weight:450;color:var(--plum)}
.t em{font-style:italic;font-weight:380;color:var(--rose)}
.g{position:absolute;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.tile{position:relative;background:#fff;border-radius:28px;display:flex;flex-direction:column;justify-content:flex-end;
  padding:18px 18px 20px;box-shadow:0 1px 0 rgba(36,16,63,.06),0 16px 30px -22px rgba(36,16,63,.35)}
.tile .n{position:absolute;top:16px;right:18px;font-family:M;font-weight:500;font-size:28px;color:#9B8BB4}
.tile .ic{position:absolute;top:20px;left:18px}
.tile .l{font-size:30px;line-height:1.1;font-weight:650;color:#2A1D40;letter-spacing:-.012em}
.tile.p{background:var(--plum)}.tile.p .l{color:var(--moon)}.tile.p .n{color:#B9A6DA}
.cta{position:absolute;font-family:H;font-size:70px;color:var(--plum);line-height:1}
"""
    ty = top if tall else 96
    gy = ty + (300 if tall else 250)
    th = 236 if tall else 190
    if kind == "tt":
        th, gy = 186, ty + 260
    tiles = ""
    for i, (ic, lab) in enumerate(GRID):
        p = False
        alt = (i // 4 + i) % 2 == 1
        tiles += f'<div class="tile{" p" if p else ""}" style="height:{th}px;{"background:#F2EBFB" if alt else ""}">{icon(ic, 56 if tall else 50, "#F7C6D3" if p else "#6B3FA0")}<div class="n">{i + 1}</div><div class="l">{e(lab)}</div></div>'
    cy = gy + 4 * th + 48 + 40
    body = f"""
<div class="t F" style="left:{L}px;right:{R}px;top:{ty}px">Which one did <em>nobody warn you about?</em></div>
<div class="g" style="left:{L - 12}px;right:{R - 12}px;top:{gy}px">{tiles}</div>
<div class="cta" style="left:{L}px;top:{cy}px">Comment the number</div>
<div class="src" style="position:absolute;{'left:' + str(L) + 'px;top:' + str(cy + 92) if kind == 'tt' else 'right:' + str(R) + 'px;top:' + str(cy + 30)}px;color:var(--plum)">All from the NHS symptom list</div>
<div class="grain"></div>"""
    return css, [body]

# ---------------------------------------------------------------------------
# Reel covers (9:16; Instagram's grid shows the middle 3:4, so text sits in y 300..1600)
# ---------------------------------------------------------------------------
def cover_day(kind):
    w, h = 1080, 1920
    css = """
.c{background:linear-gradient(180deg,#4A2A72 0%,#B4669A 55%,#F2A88C 100%);color:var(--moon)}
.clk{position:absolute;left:96px;top:470px;font-family:M;font-weight:500;font-size:190px;letter-spacing:-6px}
.t{position:absolute;left:96px;right:96px;top:760px;font-size:132px;font-weight:420}
.t em{font-style:italic;font-weight:360;color:#F7C6D3}
.moon{position:absolute;right:140px;top:330px;width:140px;height:140px;border-radius:50%;box-shadow:inset -32px 10px 0 0 #FFEFC9;transform:rotate(-20deg);filter:drop-shadow(0 0 30px rgba(255,239,201,.4))}
"""
    stars = "".join(f'<div style="position:absolute;left:{(i*263+40)%w}px;top:{120+(i*97)%700}px;width:6px;height:6px;border-radius:50%;background:#FFF3D6;opacity:{.25+(i%4)*.15:.2f}"></div>' for i in range(26))
    body = f"""{stars}<div class="sun" style="position:absolute;right:150px;top:330px;width:140px;height:140px;border-radius:50%;background:radial-gradient(circle at 40% 38%,#FFFDF6,#FFF1CF 55%,#FFD9A8);box-shadow:0 0 120px 40px rgba(255,236,200,.5)"></div><div class="clk">18:05</div>
<div class="t F">Perimenopause doesn't keep <em>office hours.</em></div>
<svg width="1080" height="1920" style="position:absolute;inset:0"><path d="M0 1700 C 260 1650, 520 1690, 760 1660 S 1000 1640, 1080 1650 L1080 1920 L0 1920Z" fill="#5B2F6E" opacity=".75"/></svg>
<div class="grain l"></div>"""
    return css, [body]
cover_day.kinds = ["tt"]

def cover_page(kind):
    w, h = 1080, 1920
    css = """
.c{background:radial-gradient(90% 55% at 100% 0%,#EFE5FC 0%,rgba(239,229,252,0) 65%),radial-gradient(80% 50% at 0% 100%,#F7DCE6 0%,rgba(247,220,230,0) 70%),linear-gradient(180deg,#E6DAF8 0%,#F1E8F7 50%,#F6E3EA 100%)}
.t{position:absolute;left:96px;right:96px;top:330px;font-size:128px;font-weight:430;color:var(--plum)}
.t em{font-style:italic;font-weight:370;color:var(--violet)}
"""
    body = f"""<div class="t F">Three months of symptoms. <em>One appointment.</em></div>
<img src="{U('img/pdf.webp')}" style="position:absolute;left:250px;top:870px;width:580px;border-radius:16px;transform:rotate(-3deg);box-shadow:0 80px 110px -50px rgba(36,16,63,.6)">
<div class="grain"></div>"""
    return css, [body]
cover_page.kinds = ["tt"]

# ---------------------------------------------------------------------------
# 8 Nov. New in 1.5.4: log a missed day, choose your reminder time
# ---------------------------------------------------------------------------
def shot(name, fallback):
    return name if (HERE / "img" / name).exists() else fallback

def feature(kind):
    w, h, tall, L, R, top, by, sy = frame(kind)
    css = """
.c{background:radial-gradient(90% 55% at 100% 0%,#FFF9E8 0%,rgba(255,249,232,0) 65%),radial-gradient(70% 50% at 0% 100%,#FBE3C8 0%,rgba(251,227,200,0) 70%),#FFF1D2;color:var(--plum)}
.t{position:absolute;font-size:118px;font-weight:440}
.t em{font-style:italic;font-weight:370;color:var(--violet)}
.b{position:absolute;font-size:44px;line-height:1.36;font-weight:480;color:#4A2F63}
.ann{position:absolute;font-family:H;font-size:64px;line-height:1;color:var(--rose);display:flex;gap:10px;align-items:flex-end}
.pill{position:absolute;display:inline-flex;align-items:center;gap:14px;padding:16px 30px 18px;border-radius:999px;background:var(--plum);color:var(--moon);font-size:36px;font-weight:650}
"""
    arrowL = '<svg width="120" height="110" viewBox="0 0 120 110" fill="none" stroke="#C8628A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M110 10 C 60 8, 22 34, 16 92"/><path d="M4 74 L16 96 L34 78"/></svg>'
    a = shot("new-day.png", "app-calendar.png")
    b = shot("new-logging.png", "app-log.png")
    c = shot("new-reminder.png", "app-home.png")
    n = 5
    pw = 500 if tall else 430
    px = (w - pw) // 2 if tall else w - R - pw + 10
    py = top + (560 if tall else 300)
    slides = []
    body = f"""
<div class="t F" style="left:{L}px;right:{R}px;top:{top}px">Missed a day? <em>Now you can fill it in.</em></div>
{phone(a, pw, f"left:{px}px;top:{py + (170 if tall else 140)}px;transform:rotate(3deg)")}
<div class="ann" style="left:{L}px;top:{py + (40 if tall else 260)}px;{'' if tall else 'width:300px;flex-direction:column;align-items:flex-start'}">tap any past day {arrowL if tall else ''}</div>
<div class="pill" style="left:{L}px;top:{by - (90 if tall else 100) if not tall else py - 110}px">New in Clari 1.5.4</div>
{foot(kind) if tall else ''}<div class="grain"></div>"""
    slides.append(body)
    steps = [
        (a, "Tap the day you missed.", "Past days in your calendar now open, even if they're empty."),
        (b, "Log it like any other day.", "The top of the screen shows which day you're filling in."),
        (c, "And choose your reminder time.", "Settings, then Daily Check-in Reminder. Pick any time that suits you."),
    ]
    for i, (img, t, sub) in enumerate(steps):
        body = f"""
<div class="t F" style="left:{L}px;right:{R}px;top:{top}px;font-size:{96 if tall else 88}px">{e(t)}</div>
<div class="b" style="left:{L}px;top:{top + (240 if tall else 220)}px;width:{820 if tall else 440}px">{e(sub)}</div>
{phone(img, pw, f"left:{px}px;top:{py if tall else top + 230}px;transform:rotate({(-3, 3, -2)[i]}deg)")}
{foot(kind, right=f"{i + 2} / {n}", mono=True)}<div class="grain"></div>"""
        slides.append(body)
    body = f"""
{mid(kind, f'''<div style="display:flex;flex-direction:column;gap:44px">
  {icon('hand-heart', 150, 'var(--violet)')}
  <div class="F" style="font-size:{116 if tall else 108}px;font-weight:440">Thank you for <em style="font-style:italic;font-weight:370;color:var(--violet)">telling us.</em></div>
  <div style="font-size:46px;line-height:1.38;font-weight:480;color:#4A2F63">Both of these came from your emails. Keep them coming: hello@clariapp.co</div></div>''')}
{foot(kind, right="Update Clari to 1.5.4")}<div class="grain"></div>"""
    slides.append(body)
    return css, slides

POSTS = {
    "2026-11-08-new": feature,
    "2026-11-11-told": thread,
    "2026-11-14-age": ruler,
    "2026-11-17-notes": notes,
    "2026-11-23-checklist": checklist,
    "2026-11-26-which-one": grid,
    "2026-11-20-reel-cover": cover_day,
    "2026-11-29-reel-cover": cover_page,
}

CHECK_JS = r"""
() => {
  const W = innerWidth, H = innerHeight, kind = document.body.dataset.kind;
  const S = JSON.parse(document.body.dataset.safe);
  const bad = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement;
    if (el.closest('.deco')) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = document.createRange(); r.selectNodeContents(n);
    for (const b of r.getClientRects()) {
      if (b.width < 1) continue;
      const rlim = (kind === 'tt' && b.bottom < 700) ? 60 : S[2];
      if (b.left < S[0] - 2 || b.top < S[1] - 2 || b.right > W - rlim + 2 || b.bottom > H - S[3] + 2)
        bad.push(`unsafe: "${n.textContent.trim().slice(0, 40)}" at ${Math.round(b.left)},${Math.round(b.top)},${Math.round(b.right)},${Math.round(b.bottom)}`);
    }
    // clipped by any ancestor with overflow hidden
    let a = el;
    while (a && a !== document.body) {
      const s = getComputedStyle(a);
      if ((s.overflow !== 'visible') && a.classList && !a.classList.contains('c')) {
        if (a.scrollHeight > a.clientHeight + 1 || a.scrollWidth > a.clientWidth + 1) bad.push(`clipped in ${a.className}: "${n.textContent.trim().slice(0, 40)}"`);
      }
      a = a.parentElement;
    }
  }
  // text boxes that overlap each other (direct text holders only)
  const holders = [...document.querySelectorAll('body *')].filter(x => [...x.childNodes].some(c => c.nodeType === 3 && c.textContent.trim()));
  const rects = holders.map(x => { const r = document.createRange(); r.selectNodeContents(x); return [x, [...r.getClientRects()]]; });
  for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < rects.length; j++) {
    const [x, A] = rects[i], [y, B] = rects[j];
    if (x.contains(y) || y.contains(x)) continue;
    for (const a of A) for (const b of B) {
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 4 && oy > 4) bad.push(`overlap: "${x.textContent.trim().slice(0, 30)}" / "${y.textContent.trim().slice(0, 30)}"`);
    }
  }
  const imgs = [...document.querySelectorAll('img, .note, .phone')].filter(i => !i.closest('.brand') && !i.closest('.deco') && !i.classList.contains('deco') && !i.closest('.note,.card,.in,.out') || i.classList.contains('note'));
  for (const [x, A] of rects) for (const im of imgs) {
    if (im.contains(x) || x.closest('.deco')) continue;
    const b = im.getBoundingClientRect();
    for (const a of A) {
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 4 && oy > 4) bad.push(`text on image: "${x.textContent.trim().slice(0, 30)}"`);
    }
  }
  return [...new Set(bad)];
}
"""

def main():
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    names = sys.argv[2:] or list(POSTS)
    kinds = ["ig", "tt"]
    tmp = HERE / "_p.html"
    problems = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name in names:
            fn = POSTS[name]
            for kind in getattr(fn, 'kinds', kinds):
                w, h = SIZES[kind]
                css, slides = fn(kind)
                pg = b.new_page(viewport={"width": w, "height": h})
                for i, body in enumerate(slides):
                    doc = page(w, h, css, body, kind).replace("<body ", f"<body data-safe='{json.dumps(SAFE[kind])}' ", 1)
                    tmp.write_text(doc)
                    pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
                    for m in pg.evaluate(CHECK_JS):
                        problems.append(f"{name} {kind} {i + 1}: {m}")
                    suffix = f"-{i + 1:02d}" if len(slides) > 1 else ""
                    pg.screenshot(path=str(out / f"{name}-{kind}{suffix}.jpg"), type="jpeg", quality=94)
                pg.close()
        b.close()
    tmp.unlink(missing_ok=True)
    print("\n".join(problems) or "all clear")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
