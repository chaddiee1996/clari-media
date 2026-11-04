"""Series: Your GP, prepared. 'Told you're too young?' Swiss-poster carousel.
Every age rule quoted from NICE guideline NG23 (recs 1.2.1, 1.2.5, 1.6.2)."""
import sys
from base import render, mark, SIZES

CSS = """
.c{font-family:Archivo}
.blue{background:#1C34C9;color:#FFD3DA}
.pink{background:#FFD3DA;color:#1C34C9}
.grain{position:absolute;inset:0;filter:url(#g);opacity:.22;mix-blend-mode:multiply;pointer-events:none}
.big{position:absolute;font-weight:900;font-stretch:62%;line-height:.78;letter-spacing:-.02em;white-space:nowrap}
.h{position:absolute;font-weight:800;font-stretch:100%;line-height:.98;letter-spacing:-.02em}
.b{position:absolute;font-weight:500;font-stretch:100%;line-height:1.3;letter-spacing:-.005em}
.lab{position:absolute;font-family:Mono;font-weight:500;font-size:26px;letter-spacing:.04em;text-transform:uppercase}
.rule{position:absolute;height:4px;background:currentColor}
.foot{position:absolute;display:flex;align-items:center;gap:12px;font-family:Archivo;font-weight:800;font-size:36px;letter-spacing:-.01em}
.q{position:absolute;font-weight:700;font-stretch:100%;line-height:1.16;letter-spacing:-.012em}
"""
DEFS = """<svg width="0" height="0" style="position:absolute"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="2"/>
<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .5 0"/></filter></svg>"""

SRC = "NICE guideline NG23"

def chrome(kind, label, idx, n, src=None):
    w, h = SIZES[kind]
    R = 150 if kind == "tt" else 64
    top = 160 if kind == "tt" else 64
    fy = h - (500 if kind == "tt" else 104)
    s = f'<div class="lab" style="left:64px;top:{top}px">{label}</div>'
    s += f'<div class="lab" style="right:{R if kind != "tt" else 60}px;top:{top}px">{idx:02d}/{n:02d}</div>'
    s += f'<div class="rule" style="left:64px;right:{R if kind != "tt" else 60}px;top:{top + 48}px"></div>'
    s += f'<div class="foot" style="left:64px;top:{fy}px">{mark(size=40)}Clari</div>'
    if src:
        s += f'<div class="lab" style="right:{R}px;top:{fy + 8}px;font-size:24px">{src}</div>'
    return s

def slides(kind):
    w, h = SIZES[kind]
    tall = h > 1500
    R = 150 if kind == "tt" else 64
    n = 7
    out = []
    t = 160 if tall else 64
    # 1 hook
    out.append(DEFS + f"""<div class="pink" style="position:absolute;inset:0">
{chrome(kind, "Your GP, prepared", 1, n)}
<div class="big" style="left:64px;top:{t + 100}px;font-size:{700 if tall else 640}px">41</div>
<div class="h" style="left:64px;right:{R}px;top:{t + (720 if tall else 660)}px;font-size:{104 if tall else 96}px">And told you’re “too young” for perimenopause?</div>
<div class="b" style="left:64px;right:{R}px;top:{t + (1080 if tall else 1010)}px;font-size:40px">Here’s what NICE, which sets NHS guidance, actually says. By age.</div>
<div class="grain"></div></div>""")
    ages = [
        ("45+", "Over 45 with symptoms",
         "NICE says perimenopause can be diagnosed from symptoms, such as hot flushes and irregular periods.",
         "No blood test needed.", "rec. 1.2.1"),
        ("40–45", "Aged 40 to 45",
         "With symptoms, including a change in your periods, NICE says a hormone blood test (FSH) can be considered.",
         "A test is an option, not a gate.", "rec. 1.2.5"),
        ("<40", "Under 40",
         "If menopause is suspected, NICE says it is diagnosed from symptoms plus two FSH blood tests, 4 to 6 weeks apart.",
         "Never diagnosed on one test alone.", "recs. 1.2.5, 1.6.2"),
    ]
    for i, (num, lab, body, punch, rec) in enumerate(ages):
        out.append(DEFS + f"""<div class="blue" style="position:absolute;inset:0">
{chrome(kind, lab, i + 2, n, f"{SRC}, {rec}")}
<div class="big" style="left:64px;top:{t + 110}px;font-size:{(560 if tall else 520) if len(num) < 4 else (430 if tall else 440)}px">{num}</div>
<div class="q" style="left:64px;right:{R}px;top:{t + (600 if tall else 560)}px;font-size:{58 if tall else 56}px">{body}</div>
<div class="h" style="left:64px;right:{R}px;top:{t + (980 if tall else 920)}px;font-size:{72 if tall else 68}px;color:#FFFFFF">{punch}</div>
<div class="grain"></div></div>""")
    # 5 what to say
    out.append(DEFS + f"""<div class="pink" style="position:absolute;inset:0">
{chrome(kind, "What to say", 5, n)}
<div class="h" style="left:64px;right:{R}px;top:{t + 120}px;font-size:{96 if tall else 92}px">Bring it back to what you’ve noticed.</div>
<div class="q" style="left:64px;right:{R}px;top:{t + (420 if tall else 400)}px;font-size:54px;border-left:10px solid #1C34C9;padding-left:36px">“I’d like to talk about perimenopause. Here’s what has changed, how often, and for how long.”</div>
<div class="b" style="left:64px;right:{R}px;top:{t + (860 if tall else 820)}px;font-size:40px">Dates and patterns are harder to dismiss than “I just don’t feel right.”</div>
<div class="grain"></div></div>""")
    # 6 the record
    out.append(DEFS + f"""<div class="blue" style="position:absolute;inset:0">
{chrome(kind, "Before you go", 6, n)}
<div class="h" style="left:64px;right:{R}px;top:{t + 120}px;font-size:{96 if tall else 92}px">Write down three things for a few weeks.</div>
<div class="q" style="left:64px;right:{R}px;top:{t + (520 if tall else 500)}px;font-size:56px;display:flex;flex-direction:column;gap:30px">
  <div><span style="font-family:Mono;font-size:34px;opacity:.75">1&nbsp;&nbsp;</span>Each symptom, and how strong</div>
  <div><span style="font-family:Mono;font-size:34px;opacity:.75">2&nbsp;&nbsp;</span>Changes to your periods</div>
  <div><span style="font-family:Mono;font-size:34px;opacity:.75">3&nbsp;&nbsp;</span>Anything that seems to set it off</div>
</div>
<div class="b" style="left:64px;right:{R}px;top:{t + (980 if tall else 940)}px;font-size:40px;color:#FFFFFF">Clari keeps that record for you and turns it into a one-page summary for your GP.</div>
<div class="grain"></div></div>""")
    # 7 save / send
    out.append(DEFS + f"""<div class="pink" style="position:absolute;inset:0">
{chrome(kind, "Keep this", 7, n)}
<div class="big" style="left:64px;top:{t + 110}px;font-size:{300 if tall else 290}px;font-stretch:62%">SAVE IT.</div>
<div class="big" style="left:64px;top:{t + (400 if tall else 380)}px;font-size:{300 if tall else 290}px;font-stretch:62%">SEND IT.</div>
<div class="h" style="left:64px;right:{R}px;top:{t + (760 if tall else 720)}px;font-size:66px">To the friend who was told she’s too young.</div>
<div class="b" style="left:64px;right:{R}px;top:{t + (980 if tall else 940)}px;font-size:38px">Clari, the private perimenopause diary. Free on the App Store and Google Play.</div>
<div class="grain"></div></div>""")
    return CSS, out

if __name__ == "__main__":
    render("young", slides, sys.argv[1])
