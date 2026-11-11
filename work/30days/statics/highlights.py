"""Instagram highlight covers (5) and new evergreen highlight stories (Start here x4, GP visit x4)."""
from common import *
import svgkit as K, os, sys
from stories import wrap, skyfill, lab, W, H, L, R, TOP, BOT

D = os.path.join(S, 'highlights')
os.makedirs(D, exist_ok=True)

# ---------------- covers ----------------
CREAM = '#FFF8EC'
PINK = '#F7B6CD'


def glyph(kind):
    cx, cy = 540, 960
    if kind == 'start':
        return f'<image href="../assets/mark.png" x="{cx-250}" y="{cy-250}" width="500" height="500"/>'
    if kind == 'symptoms':
        pts = [(cx - 200, cy - 170), (cx + 190, cy - 210), (cx + 220, cy + 160), (cx - 170, cy + 200)]
        s = ''.join(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{CREAM}" stroke-opacity=".5" stroke-width="7"/>' for x, y in pts)
        s += ''.join(f'<circle cx="{x}" cy="{y}" r="22" fill="{PINK}"/>' for x, y in pts)
        s += f'<circle cx="{cx}" cy="{cy}" r="110" fill="{CREAM}" opacity=".12"/>'
        s += f'<path d="M{cx} {cy-150} Q{cx} {cy} {cx+150} {cy} Q{cx} {cy} {cx} {cy+150} Q{cx} {cy} {cx-150} {cy} Q{cx} {cy} {cx} {cy-150}Z" fill="{CREAM}"/>'
        return s
    if kind == 'gp':
        x, y, w, h = cx - 170, cy - 230, 340, 450
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="none" stroke="{CREAM}" stroke-width="18"/>'
        s += f'<rect x="{cx-80}" y="{y-36}" width="160" height="72" rx="22" fill="{PINK}"/>'
        for k in range(3):
            yy = y + 130 + k * 100
            s += f'<path d="M{x+60} {yy} l26 26 l46 -50" fill="none" stroke="{PINK}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
            s += f'<line x1="{x+165}" y1="{yy}" x2="{x+w-60}" y2="{yy}" stroke="{CREAM}" stroke-width="16" stroke-linecap="round"/>'
        return s
    if kind == 'selfcare':
        return K.blossom(cx, cy + 20, 5.2, 0)
    if kind == 'app':
        x, y, w, h = cx - 145, cy - 270, 290, 540
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="56" fill="none" stroke="{CREAM}" stroke-width="18"/>'
        s += f'<rect x="{cx-50}" y="{y+30}" width="100" height="22" rx="11" fill="{CREAM}"/>'
        s += f'<image href="../assets/mark.png" x="{cx-95}" y="{cy-130}" width="190" height="190"/>'
        for k, ww in enumerate((150, 110)):
            s += f'<rect x="{cx-ww/2}" y="{cy+90+k*50}" width="{ww}" height="18" rx="9" fill="{PINK}" opacity="{1-k*0.35}"/>'
        return s


def cover(kind):
    svg = glyph(kind)
    js = ("function draw(){const g=c.createLinearGradient(0,0,W*0.55,H);"
          "['#7A45B5','#6233A0','#4A2180','#331762','#22103F'].forEach((s,k)=>g.addColorStop([0,.36,.66,.86,1][k],s));"
          "c.fillStyle=g;c.fillRect(0,0,W,H);"
          "const r=c.createRadialGradient(540,960,40,540,960,520);r.addColorStop(0,'rgba(249,201,216,0.30)');r.addColorStop(1,'rgba(249,201,216,0)');"
          "c.fillStyle=r;c.fillRect(0,0,W,H);CLARI.stars(c,W,H,0.5,{seed:7,n:90,bottom:1,alpha:0.5,sparkles:0});}")
    return page('cover', 1920, 1, '', js=js, svg=K.DEFS + svg)


# ---------------- Start here (night sky, logo) ----------------
START = [
    dict(lab='Start here', head='Welcome to <em>Clari.</em>', body='A private diary for perimenopause and menopause.', sky='icon', lock=True),
    dict(lab='Start here', head='Log how you feel in under a <em>minute</em> a day.', body='Symptoms, triggers, your cycle and mood. Tap, rate, done.', sky='night'),
    dict(lab='Start here', head='See your <em>patterns.</em>', body='Then take a one-page summary to your GP, made from your own notes.', sky='evening'),
    dict(lab='Start here', head='Private by <em>design.</em>', body='Your data stays on your phone. No account needed to start. Free on the App Store and Google Play.', sky='dawn', lock=True),
]


def story_start(d, k):
    lock = lockup(0, 1920, 540, BOT - 330, 660, center=True) if d.get('lock') else ''
    cells = f'''<div class="cell" style="left:0;width:{W}px;height:{H}px;padding:{TOP+40}px {R}px 0 {L}px">
        {lab(d['lab'] + f' &nbsp;{k+1}/4')}
        <h1 class="h" style="font-size:{150 if len(d['head']) < 34 else 122}px;margin-top:40px">{d['head']}</h1>
        <p class="s" style="font-size:58px;margin-top:44px;opacity:.95;line-height:1.22">{d['body']}</p></div>{lock}'''
    svg = K.hills(W, H, BOT + 40, 50, seed=k + 11, fill='#2A1150', op=.9, waves=(0.004, 0.009, 0.017))
    js = ("function draw(){" + skyfill(d['sky']) + f"CLARI.stars(c,W,H,0.5,{{seed:{k*17+3},n:200,bottom:0.85,alpha:0.7,sparkles:0}});"
          + ("" if d.get('lock') else f"CLARI.moon(c,{820 if k % 2 else 250},{1250},{110},{{glow:1}});")
          + ("" if d.get('lock') else f"CLARI.branch(c2,{1100 if k % 2 == 0 else -20},1380,2.4,{'true' if k % 2 == 0 else 'false'},0,{{}});") + "}")
    return wrap(cells, svg, js)


# ---------------- GP visit (paper notepad, numbered) ----------------
GP = [
    dict(n='', head='Before your GP appointment, <em>write these down.</em>', hand=None),
    dict(n='1', head="What's changed, and when it started.", hand='How often, and how bad.'),
    dict(n='2', head='Your periods: more often, less often, heavier, lighter.', hand='And what seems to set it off.'),
    dict(n='3', head='Then say it plainly:', hand='"I think this could be perimenopause. What are my options?"'),
]


def story_gp(d, k):
    svg = '<rect width="1080" height="1920" fill="#FBF6EE"/>'
    for y in range(0, H, 64):
        svg += f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="#F1E8DA" stroke-width="2"/>'
    svg += f'<line x1="70" x2="70" y1="0" y2="{H}" stroke="#F2B9C9" stroke-width="3"/>'
    svg += K.blossom(930, 1690, 2.6, 18) + K.blossom(1015, 1590, 1.5, -10) + K.petal(800, 1760, 1.3, 40, .9)
    svg += ('<g transform="translate(230,1720) rotate(-14)" filter="url(#softS)"><rect width="460" height="44" rx="6" fill="#C3A8EA"/><rect y="16" width="460" height="12" fill="#B096DC"/>'
            '<path d="M0 0 L-90 22 L0 44Z" fill="#F3D9B5"/><path d="M-62 15 L-90 22 L-62 29Z" fill="#241A33"/><rect x="460" width="40" height="44" fill="#CFC6D8"/><rect x="500" width="56" height="44" rx="12" fill="#F28DB2"/></g>')
    num = (f'<div style="width:150px;height:150px;border-radius:75px;background:#4A2070;display:flex;align-items:center;justify-content:center;'
           f'margin-bottom:46px"><span class="h" style="font-size:96px;color:#FFF8EC">{d["n"]}</span></div>') if d['n'] else ''
    hand = f'<p class="hand" style="font-size:{104 if len(d["hand"]) < 40 else 96}px;color:#B83A68;margin:60px 0 0;line-height:1.05">{d["hand"]}</p>' if d['hand'] else ''
    cells = f'''<div class="cell" style="left:0;width:{W}px;height:{H}px;padding:{TOP+40}px {R}px 0 {L+40}px">
        <p class="lab" style="font-size:50px;color:#B83A68;letter-spacing:.18em">GP visit &nbsp;{k+1}/4</p>
        <div style="height:90px"></div>{num}
        <h1 class="h" style="font-size:{132 if len(d['head']) < 40 else 112}px;color:#241A33">{d['head']}</h1>{hand}</div>'''
    return wrap(cells, svg, css='.h em{color:#B83A68}', light=True, bg='#FBF6EE', mark='mark-plum.png')


if __name__ == '__main__':
    jobs, outs = [], []
    def add(name, html):
        hp = os.path.join(D, name + '.html'); open(hp, 'w').write(html)
        o = os.path.join(D, name + '.png'); outs.append(o)
        jobs.append(dict(html=hp, w=1080, h=1920, slides=[dict(i=0, out=o)]))
    for kind in ('start', 'symptoms', 'gp', 'selfcare', 'app'):
        add('cover_' + kind, cover(kind))
    for k, d in enumerate(START):
        add(f'start_{k+1}', story_start(d, k))
    for k, d in enumerate(GP):
        add(f'gp_{k+1}', story_gp(d, k))
    render('highlights', jobs)
    sheet([o for o in outs if 'cover' in o], os.path.join(D, 'sheet_covers.jpg'), cols=5, w=300)
    sheet([o for o in outs if 'cover' not in o], os.path.join(D, 'sheet_stories.jpg'), cols=4, w=300)
    print('ok')
