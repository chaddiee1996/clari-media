"""Series: Peri moon (humour). 'Lost property: brain fog edition' carousel.
Kraft luggage tags on a deep green lost-property counter. Fact slide sourced from Cambridge University Hospitals NHS."""
import sys
from base import render, mark, SIZES

TAGS = [
    ("The word for “colander”", "Mid-sentence, Tuesday", "Thursday, 3am", -4.5, "#C9A57B"),
    ("Car keys", "In my hand", "In the fridge", 3.0, "#D2B088"),
    ("Why I came upstairs", "The bottom step", "Not yet", -2.5, "#C4A076"),
    ("My friend’s name. Known her 20 years", "Saying hello", "Just after she left", 3.5, "#CDAA80"),
    ("My train of thought", "Halfway through a meeting", "Still looking", -3.0, "#C7A379"),
]

CSS = """
.c{background:radial-gradient(70% 45% at 50% 0%,#2C524A 0%,rgba(44,82,74,0) 70%),radial-gradient(90% 60% at 50% 110%,#0F221E 0%,rgba(15,34,30,0) 70%),#1B3832;color:#F4EAD8}
.felt{position:absolute;inset:0;opacity:.55;mix-blend-mode:overlay;filter:url(#felt)}
.vig{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.45) 100%)}
.string{position:absolute;width:7px;background:repeating-linear-gradient(160deg,#EDE1C8 0 4px,#BFA986 4px 7px,#E2D3B4 7px 10px);border-radius:4px;box-shadow:2px 3px 4px rgba(0,0,0,.35);transform-origin:top center}
.tag{position:absolute;transform-origin:50% 0;filter:drop-shadow(0 34px 36px rgba(0,0,0,.45)) drop-shadow(0 4px 6px rgba(0,0,0,.35))}
.tag .body{position:relative;width:100%;height:100%;overflow:hidden;clip-path:polygon(16% 0,84% 0,100% 9%,100% 100%,0 100%,0 9%);border-radius:6px}
.tag .paper{position:absolute;inset:0;background:var(--k)}
.tag .tex{position:absolute;inset:0;filter:url(#paper);opacity:.55;mix-blend-mode:multiply}
.tag .fib{position:absolute;inset:0;filter:url(#fibre);opacity:.5;mix-blend-mode:multiply}
.tag .crease{position:absolute;inset:0;background:linear-gradient(102deg,rgba(0,0,0,0) 58%,rgba(0,0,0,.07) 58.4%,rgba(255,255,255,.12) 59%,rgba(0,0,0,0) 61%)}
.tag .shade{position:absolute;inset:0;background:linear-gradient(165deg,rgba(255,255,255,.22),rgba(255,255,255,0) 35%,rgba(0,0,0,.08) 100%)}
.eye{position:absolute;left:50%;width:74px;height:74px;margin-left:-37px;border-radius:50%;
  background:radial-gradient(circle,#1B3832 0 17px,#9C9C98 18px,#E8E6E0 22px,#8B8A85 30px,#5D5C58 36px,rgba(0,0,0,0) 37px)}
.rows{position:absolute;left:64px;right:64px;display:flex;flex-direction:column;gap:30px}
.row{display:flex;flex-direction:column;gap:14px;border-bottom:2px dashed rgba(60,40,20,.35);padding-bottom:18px}
.row:last-child{border-bottom:0}
.close .hw{font-size:66px}
.lab{font-family:Typer;font-size:32px;letter-spacing:.08em;color:#4A3420}
.hw{font-family:Kalam;font-weight:700;font-size:76px;line-height:1.04;color:#1D2A72;letter-spacing:-.005em;text-shadow:0 0 1px rgba(29,42,114,.35)}
.stub{position:absolute;left:0;right:0;bottom:0;height:150px;border-top:4px dotted rgba(60,40,20,.45);display:flex;justify-content:space-between;align-items:center;padding:0 60px;font-family:Typer;font-size:34px;letter-spacing:.06em;color:#4A3420;background:rgba(255,255,255,.06)}
.stamp{position:absolute;font-family:Typer;font-size:46px;letter-spacing:.08em;color:#B3261E;border:6px solid #B3261E;padding:10px 24px 6px;border-radius:8px;
  opacity:.82;mix-blend-mode:multiply;filter:url(#rough)}
.title{position:absolute;font-family:Brico;font-weight:800;font-stretch:75%;font-variation-settings:"opsz" 96;letter-spacing:-.01em;line-height:.86;color:#F4EAD8;text-transform:uppercase}
.sub{position:absolute;font-family:Kalam;font-weight:700;color:#F2C46B}
.foot{position:absolute;display:flex;align-items:center;gap:12px;font-family:Brico;font-weight:700;font-size:36px;color:#F4EAD8}
.cnt{position:absolute;font-family:Typer;font-size:30px;color:rgba(244,234,216,.7);letter-spacing:.08em}
.note{position:absolute;background:#F4EEDF;color:#1E1A14;border-radius:4px;box-shadow:0 40px 60px -20px rgba(0,0,0,.6);padding:70px 64px 64px}
.note{overflow:visible}
.pin{position:absolute;top:-22px;left:50%;margin-left:-22px;width:44px;height:44px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FF8A7A,#C0392B 55%,#7A1E16);box-shadow:0 8px 10px rgba(0,0,0,.4)}
.nh{font-family:Typer;font-size:40px;letter-spacing:.14em;color:#B3261E;margin-bottom:34px}
.nt{font-family:Brico;font-weight:700;font-stretch:88%;font-size:66px;line-height:1.06;letter-spacing:-.015em}
.nb{font-family:Fig;font-weight:500;font-size:38px;line-height:1.38;color:#3A342A;margin-top:30px}
.ns{font-family:Typer;font-size:26px;color:#6B6254;margin-top:36px;letter-spacing:.03em}
"""

DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="paper"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="4"/><feColorMatrix values="0 0 0 0 .35  0 0 0 0 .24  0 0 0 0 .12  0 0 0 .9 0"/></filter>
<filter id="fibre"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.55" numOctaves="2" seed="11"/><feColorMatrix values="0 0 0 0 .3  0 0 0 0 .2  0 0 0 0 .1  0 0 0 .55 0"/></filter>
<filter id="felt"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .35 0"/></filter>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="5"/>
<feComponentTransfer><feFuncA type="discrete" tableValues="0 1 1 1 1 0 1 1"/></feComponentTransfer></filter>
</defs></svg>"""

def bg():
    return DEFS + '<div class="felt" style="background:#fff"></div><div class="vig"></div>'

def tag(x, y, w, h, rot, color, inner, string_len=None):
    s = ""
    if string_len:
        s = f'<div class="string deco" style="left:{x + w / 2 - 1.5:.0f}px;top:{y - string_len + 40:.0f}px;height:{string_len:.0f}px;transform:rotate({rot * .4:.1f}deg)"></div>'
    return s + f"""<div class="tag obj" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);--k:{color}">
  <div class="body"><div class="paper"></div><div class="tex"></div><div class="fib"></div><div class="crease"></div><div class="shade"></div>
  <div class="eye" style="top:30px"></div>{inner}</div></div>"""

def foot(kind, right=None):
    w, h = SIZES[kind]
    y = h - (500 if kind == "tt" else 112)
    r = f'<div class="cnt" style="right:{160 if kind == "tt" else 64}px;top:{y + 6}px">{right}</div>' if right else ""
    return f'<div class="foot" style="left:64px;top:{y}px">{mark(size=40)}Clari</div>{r}'

def slides(kind):
    w, h = SIZES[kind]
    tall = h > 1500
    out = []
    # cover
    t0 = 200 if tall else 96
    cover = bg() + f"""
<div class="title" style="left:64px;right:64px;top:{t0}px;font-size:{238 if tall else 222}px">Lost<br>property</div>
{tag((w - 700) // 2 - (30 if kind == 'tt' else 0), t0 + (540 if tall else 470), 700, 580 if tall else 660, -5, "#C9A57B",
     '<div class="rows" style="top:170px"><div class="row"><div class="lab">DEPARTMENT</div><div class="hw">Brain fog</div></div><div class="row"><div class="lab">ITEMS THIS WEEK</div><div class="hw">Five. Swipe.</div></div></div>', 0)}
{foot(kind)}"""
    out.append(cover)
    n = len(TAGS) + 3
    for i, (item, seen, found, rot, col) in enumerate(TAGS):
        tw = 760
        th = 1180 if tall else 1100
        ty = 190 if tall else 110
        inner = f"""<div class="stamp" style="right:60px;top:120px;transform:rotate(-9deg)">LOST</div>
<div class="stub"><span>CLAIM No. {2711 + i * 37}</span><span>KEEP THIS HALF</span></div>
<div class="rows" style="top:{250 if tall else 230}px">
  <div class="row"><div class="lab">ITEM</div><div class="hw">{item}</div></div>
  <div class="row"><div class="lab">LAST SEEN</div><div class="hw">{seen}</div></div>
  <div class="row"><div class="lab">FOUND</div><div class="hw">{found}</div></div>
</div>"""
        body = bg() + tag((w - tw) // 2 - (30 if kind == "tt" else 0), ty, tw, th, rot, col, inner, string_len=ty + 60) + foot(kind, f"{i + 2:02d} / {n:02d}")
        out.append(body)
    # fact
    nw = 860 if kind == "ig" else 830
    fact = bg() + f"""<div class="note obj ok" style="left:{(w - nw) // 2 - (30 if kind == 'tt' else 0)}px;top:{220 if tall else 150}px;width:{nw}px;transform:rotate(-1.2deg)">
<div class="pin"></div>
<div class="nh">NOTICE</div>
<div class="nt">Problems with memory and concentration are on the NHS list of perimenopause symptoms.</div>
<div class="nb">It has a name: brain fog. It is common, and it is worth writing down when it happens.</div>
<div class="ns">Source: Cambridge University Hospitals NHS Foundation Trust</div>
</div>{foot(kind, f"{n - 1:02d} / {n:02d}")}"""
    out.append(fact)
    # close
    tw = 760
    ty = 230 if tall else 150
    inner = f"""<div class="rows close" style="top:{200 if tall else 190}px;gap:22px">
  <div class="row"><div class="lab">TO DO</div><div class="hw">Note when it happens, and how often.</div></div>
  <div class="row"><div class="lab">WHY</div><div class="hw">So your GP sees the pattern, not one bad day.</div></div>
  <div class="row"><div class="lab">SEND TO</div><div class="hw">The friend who finishes your sentences.</div></div>
</div>"""
    ty = 190 if tall else 110
    close = bg() + tag((w - tw) // 2 - (30 if kind == "tt" else 0), ty, tw, 1180 if tall else 1100, 2.0, "#E4CFA8", inner, string_len=ty + 60) + foot(kind, "CLARI, A PRIVATE SYMPTOM DIARY")
    out.append(close)
    return CSS, out

if __name__ == "__main__":
    render("lost", slides, sys.argv[1])
