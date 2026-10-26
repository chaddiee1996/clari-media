"""Clari format library: eight distinct post formats, each its own visual world.

python3 board.py OUTDIR            -> renders the style board samples
Each format is a function(data, w, h) -> html. Shared brand anchors only:
the moon mark, the plum ink, and Fraunces for display.
"""
import sys, pathlib, html
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
U = lambda p: (HERE / p).as_uri()
e = lambda t: html.escape(t or "").replace("|", "<br>")

FONTS = f"""
@font-face{{font-family:Fraunces;src:url({U('fonts/fraunces.woff2')});font-weight:100 900}}
@font-face{{font-family:Fraunces;src:url({U('fonts/fraunces-italic.woff2')});font-weight:100 900;font-style:italic}}
@font-face{{font-family:Figtree;src:url({U('fonts/figtree.woff2')});font-weight:300 900}}
@font-face{{font-family:Caveat;src:url({U('fonts/caveat.woff2')});font-weight:600}}
@font-face{{font-family:InstrumentSans;src:url({U('fonts/instrument-sans.woff2')});font-weight:400 700}}
@font-face{{font-family:InstrumentSerif;src:url({U('fonts/instrument-serif.woff2')})}}
@font-face{{font-family:InstrumentSerif;src:url({U('fonts/instrument-serif-italic.woff2')});font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{overflow:hidden}}
.s{{position:relative;overflow:hidden;-webkit-font-smoothing:antialiased}}
.grain{{position:absolute;inset:0;background:url({U('img/grain0.png')});opacity:.07;mix-blend-mode:multiply;pointer-events:none}}
.mark{{display:flex;align-items:center;gap:10px;font-family:Fraunces;font-weight:560;font-size:36px}}
.mark img{{width:34px;height:34px}}
"""

def page(w, h, css, body, bg):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
html,body{{width:{w}px;height:{h}px}} .s{{width:{w}px;height:{h}px;background:{bg}}} {css}</style></head>
<body><div class="s">{body}</div></body></html>"""

def mark(color="#2A1252"):
    return f'<div class="mark" style="color:{color}"><img src="{U("img/mark-moon.svg")}">Clari</div>'

# 1. POSTER: one fact as a giant, cropped numeral on a blush colour field
def poster(d, w, h):
    css = f"""
.big{{position:absolute;left:-28px;top:{int(h*0.06)}px;font-family:Fraunces;font-weight:300;font-size:{int(w*0.58)}px;line-height:.8;letter-spacing:-.06em;color:#2A1252;white-space:nowrap;font-variation-settings:"opsz" 144}}
.unit{{position:absolute;left:84px;top:{int(h*0.47)}px;font-family:Fraunces;font-style:italic;font-weight:300;font-size:150px;line-height:1;color:#2A1252;letter-spacing:-.03em}}
.cap{{position:absolute;left:84px;right:84px;bottom:{int(h*0.13)}px;font-family:InstrumentSans;font-weight:500;font-size:40px;line-height:1.3;color:#2A1252;max-width:760px}}
.src{{position:absolute;right:84px;bottom:64px;font-family:InstrumentSans;font-size:24px;color:#2A1252;opacity:.7}}
.m{{position:absolute;left:84px;bottom:56px}}"""
    body = f"""<div class="big">{e(d['big'])}</div><div class="unit">{e(d['unit'])}</div>
<div class="cap">{e(d['cap'])}</div><div class="src">{e(d.get('src'))}</div><div class="m">{mark()}</div><div class="grain"></div>"""
    return page(w, h, css, body, "#F3B9C9")

# 2. THREAD: lines women hear, as a message thread
def thread(d, w, h):
    css = """
.hd{position:absolute;left:84px;right:84px;top:96px;font-family:Fraunces;font-weight:450;font-size:84px;line-height:1.02;letter-spacing:-.025em;color:#1B0E33}
.th{position:absolute;left:64px;right:64px;top:360px;display:flex;flex-direction:column;gap:22px}
.b{max-width:740px;padding:28px 36px;border-radius:44px;font-family:InstrumentSans;font-size:44px;line-height:1.22;font-weight:500}
.in{align-self:flex-start;background:#E7E1EE;color:#1B0E33;border-bottom-left-radius:12px}
.out{align-self:flex-end;background:#5B2A93;color:#fff;border-bottom-right-radius:12px}
.time{align-self:center;font-family:InstrumentSans;font-size:24px;color:#7C6E90;margin:6px 0}
.ft{position:absolute;left:84px;right:84px;bottom:64px;display:flex;justify-content:space-between;align-items:center;font-family:InstrumentSans;font-size:24px;color:#7C6E90}"""
    msgs = "".join(
        f'<div class="time">{e(m[1])}</div>' if m[0] == "t" else f'<div class="b {"in" if m[0]=="in" else "out"}">{e(m[1])}</div>'
        for m in d["msgs"])
    body = f"""<div class="hd">{e(d['title'])}</div><div class="th">{msgs}</div>
<div class="ft">{mark('#1B0E33')}<span>Swipe for what the NHS says</span></div>"""
    return page(w, h, css, body, "#FBFAFD")

# 3. NOTE: a handwritten sticky note over the real photo
def note(d, w, h):
    css = f"""
.bg{{position:absolute;inset:0;background:url({U('img/' + d['img'])}) center/cover;filter:saturate(.9) brightness(.92)}}
.pn{{position:absolute;left:{int(w*0.12)}px;top:{int(h*0.2)}px;width:{int(w*0.76)}px;padding:70px 64px 80px;background:#FFE58A;
transform:rotate(-3deg);box-shadow:0 2px 0 rgba(0,0,0,.05),0 30px 50px -18px rgba(40,25,0,.45)}}
.pn::after{{content:"";position:absolute;left:0;right:0;top:0;height:46px;background:linear-gradient(180deg,rgba(0,0,0,.06),rgba(0,0,0,0))}}
.hw{{font-family:Caveat;font-weight:600;font-size:92px;line-height:1.04;color:#1E2A4A}}
.hw u{{text-decoration:none;background:linear-gradient(transparent 62%,rgba(232,98,143,.45) 62%)}}
.tag{{position:absolute;left:84px;bottom:64px}}
.src{{position:absolute;right:84px;bottom:70px;font-family:InstrumentSans;font-size:24px;color:#fff;opacity:.85}}"""
    body = f"""<div class="bg"></div><div class="pn"><div class="hw">{d['note']}</div></div>
<div class="tag">{mark('#FFFFFF')}</div><div class="src">{e(d.get('src'))}</div>"""
    return page(w, h, css, body, "#222")

# 4. CARD: a saveable appointment checklist card
def card(d, w, h):
    rows = "".join(f'<div class="r"><div class="k">{e(k)}</div><div class="v">{e(v)}</div></div>' for k, v in d["rows"])
    css = """
.c{position:absolute;left:72px;right:72px;top:50%;transform:translateY(-54%);background:#FFFDF8;border-radius:28px;padding:64px 64px 40px;
box-shadow:0 40px 80px -40px rgba(42,18,82,.55)}
.t{font-family:InstrumentSerif;font-size:100px;line-height:.98;color:#1B0E33;letter-spacing:-.01em}
.t i{font-style:italic}
.r{display:grid;grid-template-columns:150px 1fr;gap:24px;padding:28px 0;border-top:2px solid #E9E2F2}
.r:first-of-type{margin-top:44px}
.k{font-family:InstrumentSans;font-weight:700;font-size:26px;color:#8A5BC4;padding-top:8px}
.v{font-family:InstrumentSans;font-size:42px;line-height:1.25;color:#1B0E33}
.ft{position:absolute;left:84px;right:84px;bottom:56px;display:flex;justify-content:space-between;align-items:center;font-family:InstrumentSans;font-size:24px;color:#2A1252}"""
    body = f"""<div class="c"><div class="t">{d['title']}</div>{rows}</div>
<div class="ft">{mark()}<span>{e(d.get('src'))}</span></div><div class="grain"></div>"""
    return page(w, h, css, body, "linear-gradient(160deg,#CDB8F0 0%,#E9C9E6 100%)")

# 5. ZOOM: the real app UI, cropped huge on deep plum
def zoom(d, w, h):
    css = f"""
.t{{position:absolute;left:84px;right:84px;top:96px;font-family:Fraunces;font-weight:420;font-size:96px;line-height:1.0;letter-spacing:-.03em;color:#FFF3D6}}
.sub{{position:absolute;left:84px;right:84px;top:{int(h*0.36)}px;font-family:InstrumentSans;font-size:40px;line-height:1.3;color:#D8C6F5;max-width:760px}}
.ui{{position:absolute;left:-60px;width:{int(w*1.32)}px;bottom:{int(h*0.12)}px;border-radius:36px;
box-shadow:0 60px 120px -40px rgba(0,0,0,.7);transform:rotate(-5deg)}}
.m{{position:absolute;left:84px;bottom:56px}}"""
    body = f"""<div class="t">{e(d['title'])}</div><div class="sub">{e(d['sub'])}</div>
<img class="ui" src="{U('img/ui-tiles.png')}"><div class="m">{mark('#FFF3D6')}</div>"""
    return page(w, h, css, body, "radial-gradient(120% 70% at 80% 100%,#5B2A93 0%,#2A1252 45%,#140A2B 100%)")

# 6. EDITORIAL: full-bleed photo, magazine caption strip
def editorial(d, w, h):
    css = f"""
.bg{{position:absolute;inset:0;background:url({U('img/' + d['img'])}) {d.get('pos','center')}/cover}}
.strip{{position:absolute;left:0;right:0;bottom:0;background:#FFF9F2;padding:44px 84px 56px}}
.t{{font-family:InstrumentSerif;font-size:88px;line-height:1.0;color:#1B0E33}}
.t i{{font-style:italic}}
.row{{display:flex;justify-content:space-between;align-items:center;margin-top:28px;font-family:InstrumentSans;font-size:26px;color:#5A4775}}"""
    body = f"""<div class="bg"></div><div class="strip"><div class="t">{d['title']}</div>
<div class="row">{mark('#1B0E33')}<span>{e(d.get('sub'))}</span></div></div>"""
    return page(w, h, css, body, "#000")

# 7. SPLIT: myth on top, fact underneath, hard colour break
def split(d, w, h):
    css = f"""
.top{{position:absolute;left:0;right:0;top:0;height:{int(h*0.46)}px;background:#FFF3D6;padding:110px 84px 0}}
.bot{{position:absolute;left:0;right:0;bottom:0;top:{int(h*0.46)}px;background:#2A1252;padding:90px 84px 0}}
.lab{{font-family:InstrumentSans;font-weight:700;font-size:30px;margin-bottom:22px}}
.top .lab{{color:#C8628A}} .bot .lab{{color:#F3B9C9}}
.myth{{font-family:InstrumentSerif;font-style:italic;font-size:118px;line-height:.98;color:#2A1252;text-decoration:line-through;text-decoration-color:#E8628F;text-decoration-thickness:7px}}
.fact{{font-family:InstrumentSans;font-weight:600;font-size:52px;line-height:1.22;color:#FFF3D6;max-width:860px}}
.src{{position:absolute;left:84px;right:84px;bottom:60px;display:flex;justify-content:space-between;align-items:center;font-family:InstrumentSans;font-size:24px;color:#CDB8F0}}"""
    body = f"""<div class="top"><div class="lab">They say</div><div class="myth">{e(d['myth'])}</div></div>
<div class="bot"><div class="lab">The NHS says</div><div class="fact">{e(d['fact'])}</div></div>
<div class="src">{mark('#FFF3D6')}<span>{e(d.get('src'))}</span></div>"""
    return page(w, h, css, body, "#2A1252")

# 8. QUESTION: a single big open question, typographic, lilac
def question(d, w, h):
    css = f"""
.q{{position:absolute;left:84px;right:84px;top:{int(h*0.14)}px;font-family:Fraunces;font-weight:300;font-size:136px;line-height:.95;letter-spacing:-.04em;color:#2A1252;font-variation-settings:"opsz" 144}}
.q b{{font-weight:600}}
.cta{{position:absolute;left:84px;bottom:{int(h*0.12)}px;font-family:Caveat;font-size:72px;color:#5B2A93;transform:rotate(-2deg)}}
.m{{position:absolute;right:84px;bottom:56px}}"""
    body = f"""<div class="q">{d['q']}</div><div class="cta">{e(d['cta'])}</div><div class="m">{mark()}</div><div class="grain"></div>"""
    return page(w, h, css, body, "#D9CBF4")

SAMPLES = [
    ("poster", poster, {"big": "7–9", "unit": "years", "cap": "How long perimenopause symptoms usually last. Sometimes longer.", "src": "Source: nhs.uk"}),
    ("thread", thread, {"title": "Things women still hear", "msgs": [("in", "You're too young for that."), ("in", "It's probably just stress."), ("t", "Three months later"), ("out", "I've written down every night sweat since August."), ("in", "Ok, let's talk about this properly.")]}),
    ("note", note, {"img": "notes.jpg", "note": "Ask reception <u>which GP</u> is best for menopause.<br>And book a longer slot!", "src": "Tip from Nuffield Health"}),
    ("card", card, {"title": "Your GP <i>appointment</i>", "rows": [("Bring", "Notes on each symptom: how often, how strong"), ("Say", "“I think this could be perimenopause.”"), ("Ask", "“What are my options?”"), ("Know", "Over 45? NICE says no blood test is needed to diagnose it.")], "src": "Sources: Nuffield Health, NICE NG23"}),
    ("zoom", zoom, {"title": "Tap once. Tap again.", "sub": "The moon fills as a symptom gets stronger. That's the whole idea."}),
    ("editorial", editorial, {"img": "dawn.jpg", "pos": "center 30%", "title": "Walk in with <i>the whole picture.</i>", "sub": "Clari: a private symptom diary"}),
    ("split", split, {"myth": "“It's over in a year.”", "fact": "Symptoms usually last 7 to 9 years, sometimes longer, and they change along the way.", "src": "Source: nhs.uk"}),
    ("question", question, {"q": "What do you <b>wish</b> your GP knew about perimenopause?", "cta": "Tell us below ↓"}),
]

def render(items, out, sizes=((1080, 1350, "ig"),)):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    tmp = HERE / "_b.html"
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w, h, tag in sizes:
            pg = b.new_page(viewport={"width": w, "height": h})
            for name, fn, d in items:
                tmp.write_text(fn(d, w, h)); pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
                pg.screenshot(path=str(out / f"{name}-{tag}.jpg"), type="jpeg", quality=93)
        b.close()
    tmp.unlink(missing_ok=True)

if __name__ == "__main__":
    render(SAMPLES, sys.argv[1])
