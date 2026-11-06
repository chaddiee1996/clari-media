from common import *
import svgkit as K, math, json, os, sys
sys.path.insert(0, S)
from c3 import objects as c3objects

F9 = FMT[1920]
W, H = 1080, 1920
L, R = 88, 170
TOP = 330          # first text line (mark sits at 230)
BOT = 1500         # nothing below this

STORIES = [
    ('2026-11-09', 'K', dict(q="New week. First question: how did you sleep last night?", note='#F7B6CD', rot=-3, obj='pencil')),
    ('2026-11-10', 'T', dict(reel='R1', line='<em>3:07am.</em> Duvet off. Duvet on.', still='bedroom', img='still_r1.jpg')),
    ('2026-11-11', 'N', dict(name='Night sweats', sub='Hot flushes that happen at night.', sky='night', seed=1)),
    ('2026-11-12', 'T', dict(reel='R2', line='Told you\'re too young for perimenopause? What NICE says, <em>by age.</em>', still='paper41', img='still_r2.jpg')),
    ('2026-11-13', 'A', dict(line='Tap a symptom, then how strong it was. That\'s the whole <em>check-in.</em>', screen='log.png', sky='night', rot=-5)),
    ('2026-11-14', 'N', dict(name='Joint aches and muscle pains', sub=None, sky='evening', seed=2)),
    ('2026-11-15', 'K', dict(q="Sunday check-in: what was the hardest bit of this week? Write it down.", note='#DCC8F5', rot=2.5, obj='clip')),
    ('2026-11-16', 'W', dict(day=1, line='Self Care Week starts today. 16 to 22 <em>November.</em>', obj='windows', sun=0.92)),
    ('2026-11-17', 'W', dict(day=2, line='Go to bed at the <em>same</em> time as last night.', obj='pillow', sun=0.78)),
    ('2026-11-18', 'W', dict(day=3, line='A walk while it\'s still <em>light.</em>', obj='path', sun=0.62)),
    ('2026-11-19', 'W', dict(day=4, line='Tell one person how you\'re <em>really</em> doing.', obj='mugs', sun=0.50)),
    ('2026-11-20', 'W', dict(day=5, line='Ten <em>quiet</em> minutes. Yoga, tai chi, or meditation.', obj='candle', sun=0.56)),
    ('2026-11-21', 'W', dict(day=6, line='Something with <em>calcium.</em> Milk, yoghurt, kale.', obj='milk', sun=0.70)),
    ('2026-11-22', 'W', dict(day=7, line='Write down how this week really <em>felt.</em>', obj='book', sun=0.86)),
    ('2026-11-23', 'N', dict(name='Headaches and migraines', sub='worse than usual', sky='icon', seed=3)),
    ('2026-11-24', 'A', dict(line='Your week, as <em>moons.</em> One for every day you log.', screen='home.png', sky='evening', rot=4, top=830)),
    ('2026-11-25', 'N', dict(name='Sensitive teeth and sore gums', sub='Yes, really.', sky='dawn', seed=4)),
    ('2026-11-26', 'A', dict(line='Your data stays on your phone. No account needed to <em>start.</em>', screen='homelogged.png', sky='icon', rot=-3)),
    ('2026-11-27', 'N', dict(name='Dry, itchy skin', sub=None, sky='plum', seed=5)),
    ('2026-11-28', 'K', dict(q="Heating on? NHS tip: keep your bedroom cool at night.", note='#CFE0F7', rot=-2, obj='blossom', src='Source: NHS')),
    ('2026-11-29', 'K', dict(q="Sunday check-in: anything new this week? A new symptom, a new pattern?", note='#FFE7A8', rot=3, obj='mug')),
    ('2026-11-30', 'N', dict(name='A change to your periods', sub='Usually one of the first signs.', sky='night', seed=6)),
    ('2026-12-01', 'K', dict(q="December. Party season. Notice what sets your flushes off.", note='#FFD3B5', rot=-3.5, obj='tape')),
    ('2026-12-02', 'N', dict(name='Palpitations', sub='The NHS says to contact your GP about them.', sky='evening', seed=7)),
    ('2026-12-03', 'A', dict(line='A one-page summary for your GP, made from your own <em>notes.</em>', screen='summary.png', sky='night', rot=5)),
    ('2026-12-04', 'N', dict(name='Hair thinning', sub=None, sky='icon', seed=8)),
    ('2026-12-05', 'K', dict(q="Christmas list idea: a cold water bottle by the bed. Not festive. Very useful.", note='#F9D2E0', rot=2, obj='pencil2')),
    ('2026-12-06', 'K', dict(q="Sunday check-in: how has your sleep been this week?", note='#E6DAFA', rot=-2.5, obj='clip2')),
    ('2026-12-07', 'N', dict(name='Menopause', sub='12 months without a period. Before that, it\'s perimenopause.', sky='dawn', seed=9)),
    ('2026-12-08', 'T', dict(reel='R13', line='A new question at your NHS <em>Health Check.</em>', still='letter', img='still_r13.jpg')),
]

SKY_JS = {
    'night': "['#120723','#2C1252','#4A2180','#6F3FA6','#8E57BE']",
    'evening': "['#150929','#391766','#7742AE','#C47CBD','#F7B9CB']",
    'icon': "['#0E061D','#22103F','#3C1A6E','#5D3194','#7A45B5']",
    'dawn': "['#2A1858','#5A3A98','#A86BB0','#E79BA8','#FFC9A8']",
    'plum': "['#1A0A33','#3A1766','#5A2A8C','#8A4FA8','#C67FB4']",
}


def wrap(cells, svg='', js='', css='', light=False, bg='#22103F', mark='mark.png', src=None):
    chrome_ = f'<img class="chrome-mark" src="../assets/{mark}" style="left:{L}px;top:230px">'
    if src:
        chrome_ += f'<p class="src" style="left:{L}px;top:{BOT-60}px">{src}</p>'
    return page('Clari story', 1920, 1, cells + chrome_, js=js, svg=K.DEFS + svg, css=css, light=light, bg=bg)


def skyfill(key):
    return f"const g=c.createLinearGradient(0,0,0,H); const s={SKY_JS[key]}; [0,.36,.66,.86,1].forEach((p,k)=>g.addColorStop(p,s[k])); c.fillStyle=g; c.fillRect(0,0,W,H);"


def lab(t, col='var(--pink)'):
    return f'<p class="lab" style="font-size:50px;color:{col};letter-spacing:.18em">{t}</p>'


# ---------------- N: On the NHS list ----------------
def story_N(d):
    rnd = __import__('random').Random(d['seed'] * 97)
    sx, sy = 640 + rnd.randint(-60, 120), 640 + rnd.randint(-40, 60)
    # a small, different constellation around the star each day
    pts = [(sx, sy)]
    ang = rnd.uniform(0, 6.28)
    for k in range(4):
        ang += rnd.uniform(0.9, 1.7)
        r = rnd.uniform(170, 300)
        pts.append((min(W - 80, max(L + 40, sx + r * math.cos(ang))), min(860, max(380, sy + r * math.sin(ang) * 0.7))))
    svg = ''.join(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#FFF8EC" stroke-opacity=".4" stroke-width="3"/>' for a, b in zip(pts, pts[1:]))
    svg += ''.join(K.star(x, y, r=6, glow=36, arms=20, op=.85) for x, y in pts[1:])
    svg += f'<circle cx="{sx}" cy="{sy}" r="360" fill="url(#glowHot)" opacity=".75"/>' + K.sparkle(sx, sy, 120, '#FFF6E2') + f'<circle cx="{sx}" cy="{sy}" r="20" fill="#FFFDF6"/>'
    svg += K.hills(W, H, BOT + 60, 50, seed=d['seed'], fill='#2A1150', op=.9, waves=(0.004, 0.009, 0.017))
    name = d['name']
    size = 168 if len(name) < 14 else (140 if len(name) < 26 else 124)
    sub = f'<p class="h" style="font-size:{72 if len(d["sub"]) < 30 else 60}px;font-style:italic;font-weight:600;color:var(--pink);margin-top:34px;line-height:1.1">{d["sub"]}</p>' if d['sub'] else ''
    cells = f'''<div class="cell" style="left:0;width:{W}px;height:{H}px;padding:{TOP+40}px {R}px {H-BOT+110}px {L}px">
        {lab('On the NHS list')}
        <div style="flex:1"></div>
        <h1 class="h" style="font-size:{size}px;line-height:1.0">{name}</h1>{sub}</div>'''
    js = "function draw(){" + skyfill(d['sky']) + f"CLARI.stars(c,W,H,0.5,{{seed:{d['seed']*13},n:200,bottom:0.8,alpha:0.85,sparkles:8}});" + "}"
    return wrap(cells, svg, js, src='Source: NHS')


# ---------------- K: Check-in (paper) ----------------
def story_K(d):
    q = d['q']
    size = 110 if len(q) < 56 else (98 if len(q) < 72 else 90)
    objs = {
        'pencil': '<g transform="translate(700,1440) rotate(-28)" filter="url(#softS)"><rect width="520" height="44" rx="6" fill="#C3A8EA"/><rect y="16" width="520" height="12" fill="#B096DC"/><path d="M0 0 L-90 22 L0 44Z" fill="#F3D9B5"/><path d="M-62 15 L-90 22 L-62 29Z" fill="#241A33"/><rect x="520" width="40" height="44" fill="#CFC6D8"/><rect x="560" width="56" height="44" rx="12" fill="#F28DB2"/></g>',
        'pencil2': '<g transform="translate(160,560) rotate(62)" filter="url(#softS)"><rect width="460" height="44" rx="6" fill="#F7B6CD"/><rect y="16" width="460" height="12" fill="#EE9DBA"/><path d="M0 0 L-90 22 L0 44Z" fill="#F3D9B5"/><path d="M-62 15 L-90 22 L-62 29Z" fill="#241A33"/><rect x="460" width="40" height="44" fill="#CFC6D8"/><rect x="500" width="56" height="44" rx="12" fill="#C3A8EA"/></g>',
        'clip': '<path d="M770 420 L770 300 Q770 250 820 250 Q870 250 870 300 L870 470 Q870 530 810 530 Q750 530 750 470 L750 330" fill="none" stroke="#8A7A9C" stroke-width="10" stroke-linecap="round"/>',
        'clip2': '<path d="M300 420 L300 300 Q300 250 350 250 Q400 250 400 300 L400 470 Q400 530 340 530 Q280 530 280 470 L280 330" fill="none" stroke="#B83A68" stroke-width="10" stroke-linecap="round"/>',
        'blossom': K.blossom(860, 1400, 2.6, 18) + K.blossom(960, 1300, 1.6, -10) + K.petal(760, 1480, 1.3, 40, .9),
        'mug': '<circle cx="860" cy="1430" r="170" fill="none" stroke="#C79A6B" stroke-opacity=".22" stroke-width="20" stroke-dasharray="600 60 260 80"/>',
        'tape': '',
    }
    tape_col = {'pencil': '#C3A8EA', 'clip': '#F7B6CD', 'blossom': '#F7B6CD', 'mug': '#C3A8EA', 'tape': '#E8628F', 'pencil2': '#FFE29A', 'clip2': '#C3A8EA'}[d['obj']]
    svg = '<rect width="1080" height="1920" fill="#FBF6EE"/>'
    for y in range(0, H, 64):
        svg += f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="#F1E8DA" stroke-width="2"/>'
    note = (f'<div class="abs" style="left:110px;top:470px;width:800px;height:880px;background:linear-gradient(165deg,{d["note"]},{d["note"]}DD);'
            f'transform:rotate({d["rot"]}deg);box-shadow:0 26px 40px rgba(36,26,51,.20), 0 2px 0 rgba(0,0,0,.04);padding:110px 80px 70px;box-sizing:border-box;display:flex;flex-direction:column">'
            f'<div style="position:absolute;left:300px;top:-30px;width:200px;height:62px;background:{tape_col};opacity:.75;transform:rotate({-d["rot"]*1.4}deg)"></div>'
            f'<p class="lab" style="font-size:48px;color:#B83A68;letter-spacing:.18em">Check-in</p>'
            f'<p class="hand" style="font-size:{size}px;color:#241A33;margin:30px 0 0;line-height:1.02">{q}</p>'
            f'<div style="flex:1"></div>'
            + ''.join('<div style="height:4px;background:rgba(36,26,51,.18);margin-top:58px;border-radius:2px"></div>' for _ in range(2)) +
            '</div>')
    return wrap(note, svg + objs[d['obj']], css='', light=True, bg='#FBF6EE', mark='mark-plum.png', src=d.get('src'))


# ---------------- W: Self Care Week ----------------
DAWN = ['#2E1C62', '#6A46A8', '#C982B6', '#F6AFA6', '#FFDDB5']


def story_W(d):
    day = d['day']
    # each day the dawn gets a little lighter
    t = (day - 1) / 6
    def mix(a, b, t):
        a = [int(a[i:i+2], 16) for i in (1, 3, 5)]; b = [int(b[i:i+2], 16) for i in (1, 3, 5)]
        return '#' + ''.join(f'{round(x+(y-x)*t):02X}' for x, y in zip(a, b))
    light = ['#5A4BB8', '#8C73CF', '#D99BC6', '#FAC2B4', '#FFE6C8']
    pal = [mix(a, b, t * 0.8) for a, b in zip(DAWN, light)]
    sunx = W * d['sun']
    suny = 1470 - 60 * math.sin(t * math.pi)
    OB = c3objects()
    svg = K.hills(W, H, 1450, 60, seed=day * 0.9, fill='#7A4FA8', op=.8, waves=(0.003, 0.007, 0.013)) + K.hills(W, H, 1580, 30, seed=day * 1.7, fill='#3E1C6C', waves=(0.0025, 0.006, 0.012))
    if d['obj'] == 'windows':
        ww, gap, wy, wh = 96, 10, 1330, 230
        x0 = W - R - (7 * ww + 6 * gap)
        x0 = (W - (7 * ww + 6 * gap)) / 2 + 60
        for k in range(7):
            x = x0 + k * (ww + gap)
            svg += (f'<path d="M{x},{wy+wh} L{x},{wy+ww/2} A{ww/2},{ww/2} 0 0 1 {x+ww},{wy+ww/2} L{x+ww},{wy+wh} Z" fill="{"#FFE6C8" if k == 0 else "#3E1C6C"}" stroke="#FFF8EC" stroke-opacity=".7" stroke-width="3"/>')
    else:
        sc = 0.66 if d['obj'] not in ('path',) else 0.7
        svg += f'<g transform="translate({W*0.62:.0f},1600) scale({sc})">{OB[d["obj"]]}</g>'
    big = f'<span class="h" style="font-size:380px;line-height:.78;font-weight:800">{day}</span>'
    cells = f'''<div class="cell" style="left:0;width:{W}px;height:{H}px;padding:{TOP+40}px {R}px {H-BOT}px {L}px">
        {lab('Self Care Week')}
        <div style="display:flex;align-items:flex-end;gap:24px;margin-top:40px">{big}<span class="lab" style="font-size:60px;color:var(--cream);letter-spacing:.14em;margin-bottom:20px">Day</span></div>
        <h2 class="h" style="font-size:{112 if len(d["line"]) < 45 else 100}px;margin-top:44px">{d["line"]}</h2></div>'''
    js = ("function draw(){ const g=c.createLinearGradient(0,0,0,H); const s=" + json.dumps(pal) + "; [0,.36,.66,.86,1].forEach((p,k)=>g.addColorStop(p,s[k])); c.fillStyle=g; c.fillRect(0,0,W,H);"
          f"CLARI.stars(c,W,H,0.5,{{seed:{day*7},n:110,bottom:0.4,alpha:{0.8-0.6*t:.2f},sparkles:5}});"
          f"const x={sunx:.0f}, y={suny:.0f}, r=110; const gl=c.createRadialGradient(x,y,r*0.4,x,y,r*4.5); gl.addColorStop(0,'rgba(255,236,190,0.6)'); gl.addColorStop(1,'rgba(255,236,190,0)'); c.fillStyle=gl; c.fillRect(0,0,W,H);"
          "const dd=c.createRadialGradient(x-r*0.3,y-r*0.3,r*0.1,x,y,r); dd.addColorStop(0,'#FFFBEA'); dd.addColorStop(1,'#FFD9A0'); c.fillStyle=dd; c.beginPath(); c.arc(x,y,r,0,Math.PI*2); c.fill(); }")
    return wrap(cells, svg, js, src=None)


# ---------------- A: From the app ----------------
def story_A(d):
    pw = 470
    ph = pw * 2796 / 1290
    cells = f'''<div class="cell" style="left:0;width:{W}px;height:{H}px;padding:{TOP+40}px {R}px 0 {L}px">
        {lab('From the app')}
        <h2 class="h" style="font-size:{110 if len(d["line"]) < 62 else 100}px;margin-top:34px">{d["line"]}</h2></div>'''
    px = 300 if d['rot'] < 0 else 330
    cells += f'<div class="abs" style="left:{px}px;top:{d.get("top",1000)}px">{phone(d["screen"], pw, rot=d["rot"])}</div>'
    # hills in front of the phone, so it rises out of the Clari landscape and stays above the bottom zone
    svg = ''
    fg = K.hills(W, H, 1590, 40, seed=d['rot'], fill='#4A2180', op=.95, waves=(0.003, 0.007, 0.013)) + K.hills(W, H, 1670, 30, seed=d['rot'] * 2, fill='#1C0B36', waves=(0.0028, 0.006, 0.012))
    cells += f'<svg class="abs" style="left:0;top:0" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{fg}</svg>'
    js = ("function draw(){" + skyfill(d['sky']) + "CLARI.stars(c,W,H,0.5,{seed:" + str(abs(int(d['rot'] * 10))) + ",n:220,bottom:0.8,alpha:0.8,sparkles:8});"
          + ("CLARI.moon(c, 900, 1060, 120, {glow:1});" if d['rot'] < 0 else "CLARI.moon(c, 190, 1080, 120, {glow:1});")
          + ("CLARI.branch(c2, 1100, 1380, 2.6, true, 0, {});" if d['rot'] < 0 else "CLARI.branch(c2, -20, 1370, 2.6, false, 0, {});") + "}")
    return wrap(cells, svg, js)


# ---------------- T: Today on our feed ----------------
def still_svg(kind, w, h):
    """teaser frames drawn from the reel briefs, in the Clari world (swap for real reel stills when they exist)."""
    if kind == 'bedroom':
        return (f'<defs><linearGradient id="rm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A1552"/><stop offset="1" stop-color="#160A2E"/></linearGradient>'
                f'<linearGradient id="win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120723"/><stop offset="1" stop-color="#4A2180"/></linearGradient></defs>'
                f'<rect width="{w}" height="{h}" fill="url(#rm)"/>'
                f'<rect x="{w*0.52}" y="{h*0.08}" width="{w*0.38}" height="{h*0.36}" rx="10" fill="url(#win)" stroke="#4A2A72" stroke-width="14"/>'
                + K.moon_phase(w * 0.76, h * 0.2, 46, 'wane') +
                ''.join(K.sparkle(w * a, h * b, 9, op=.8) for a, b in [(0.6, 0.14), (0.84, 0.34), (0.66, 0.32)]) +
                f'<rect x="0" y="{h*0.70}" width="{w}" height="{h*0.30}" fill="#1A0B33"/>'
                f'<path d="M{w*0.0} {h*0.66} L{w*0.55} {h*0.66} Q{w*0.6} {h*0.66} {w*0.6} {h*0.72} L{w*0.6} {h*0.9} L0 {h*0.9}Z" fill="#6A3BA0"/>'
                f'<path d="M0 {h*0.69} L{w*0.5} {h*0.69} Q{w*0.62} {h*0.75} {w*0.56} {h*0.97} L0 {h*0.97}Z" fill="#C3A8EA" opacity=".9"/>'
                f'<rect x="{w*0.66}" y="{h*0.60}" width="{w*0.30}" height="{h*0.30}" rx="12" fill="#3A1D63"/>'
                f'<rect x="{w*0.64}" y="{h*0.46}" width="{w*0.34}" height="{h*0.15}" rx="22" fill="#4A2A72"/>'
                f'<rect x="{w*0.665}" y="{h*0.475}" width="{w*0.29}" height="{h*0.095}" rx="12" fill="#12071F"/>'
                f'<text x="{w*0.81}" y="{h*0.553}" text-anchor="middle" font-family="Figtree" font-weight="800" font-size="{h*0.075:.0f}" fill="#F7B6CD" letter-spacing="2">3:07</text>'
                f'<circle cx="{w*0.81}" cy="{h*0.52}" r="{w*0.3}" fill="url(#glowP)" opacity=".35"/>')
    if kind == 'paper41':
        return (f'<rect width="{w}" height="{h}" fill="#FBF6EE"/>'
                + ''.join(f'<line x1="0" x2="{w}" y1="{y}" y2="{y}" stroke="#E8DFEF" stroke-width="2"/>' for y in range(40, int(h), 56)) +
                f'<text x="{w*0.92}" y="{h*0.56}" text-anchor="end" font-family="Fraunces" font-weight="800" font-size="{h*0.46:.0f}" fill="#241A33" letter-spacing="-8">41.</text>'
                f'<path d="M{w*0.28} {h*0.62} C{w*0.45} {h*0.60} {w*0.7} {h*0.63} {w*0.9} {h*0.61}" stroke="#B83A68" stroke-width="10" fill="none" stroke-linecap="round"/>'
                f'<g transform="translate({w*0.12},{h*0.84}) rotate(-14)"><rect width="{w*0.62}" height="30" rx="5" fill="#C3A8EA"/><path d="M0 0 L-60 15 L0 30Z" fill="#F3D9B5"/><path d="M-40 10 L-60 15 L-40 20Z" fill="#241A33"/><rect x="{w*0.62}" width="40" height="30" rx="8" fill="#F28DB2"/></g>')
    if kind == 'letter':
        return (f'<defs><linearGradient id="dn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A52B4"/><stop offset=".6" stop-color="#E79BB0"/><stop offset="1" stop-color="#FFDDB5"/></linearGradient></defs>'
                f'<rect width="{w}" height="{h}" fill="url(#dn)"/>'
                f'<rect x="{w*0.14}" y="{h*0.06}" width="{w*0.72}" height="{h*0.94}" rx="18" fill="#4A2070"/>'
                f'<rect x="{w*0.20}" y="{h*0.12}" width="{w*0.60}" height="{h*0.30}" rx="10" fill="#5E2E8E"/><rect x="{w*0.20}" y="{h*0.50}" width="{w*0.60}" height="{h*0.42}" rx="10" fill="#5E2E8E"/>'
                f'<rect x="{w*0.30}" y="{h*0.43}" width="{w*0.40}" height="{h*0.055}" rx="8" fill="#C9BFD6"/><rect x="{w*0.32}" y="{h*0.455}" width="{w*0.36}" height="{h*0.012}" fill="#2A1548"/>'
                f'<g transform="translate({w*0.5},{h*0.62}) rotate(-8)" filter="url(#soft)"><rect x="{-w*0.26}" y="{-h*0.10}" width="{w*0.52}" height="{h*0.22}" rx="10" fill="#FFF8EC"/>'
                f'<path d="M{-w*0.26} {-h*0.10} L0 {h*0.01} L{w*0.26} {-h*0.10}" fill="none" stroke="#E2D2C4" stroke-width="6"/>'
                f'<rect x="{w*0.14}" y="{-h*0.085}" width="{w*0.09}" height="{h*0.07}" rx="4" fill="#E8628F"/></g>'
                f'<circle cx="{w*0.5}" cy="{h*0.2}" r="{w*0.5}" fill="url(#glowW)" opacity=".25"/>')
    return ''


def story_T(d):
    fw, fh = 600, 750
    fx, fy = 190, 480
    st = still_svg(d['still'], fw, fh)
    frame = (f'<div class="abs" style="left:{fx}px;top:{fy}px;width:{fw}px;height:{fh}px;border-radius:36px;overflow:hidden;transform:rotate(-2.5deg);'
             f'box-shadow:0 40px 80px rgba(16,4,40,.5), 0 0 0 14px #FFF8EC">'
             + (f'<img src="../assets/{d["img"]}" style="display:block;width:{fw}px;height:{fh}px;object-fit:cover">' if d.get('img') else f'<svg width="{fw}" height="{fh}" viewBox="0 0 {fw} {fh}" xmlns="http://www.w3.org/2000/svg">{K.DEFS}{st}</svg>') +
             f'<div style="position:absolute;left:36px;bottom:36px;width:110px;height:110px;border-radius:50%;background:rgba(255,248,236,.88);display:flex;align-items:center;justify-content:center">'
             f'<svg width="44" height="48" viewBox="0 0 60 64"><path d="M8 4 L56 32 L8 60Z" fill="#4A2070"/></svg></div></div>')
    pill = (f'<div class="abs" style="left:{fx+fw-200}px;top:{fy+fh-50}px;transform:rotate(4deg);background:#F7B6CD;border-radius:60px;padding:22px 40px;box-shadow:0 14px 30px rgba(16,4,40,.35)">'
            f'<p class="lab" style="font-size:48px;color:#22103F;letter-spacing:.12em">New post</p></div>')
    cells = f'''<div class="cell" style="left:0;width:{W}px;height:{H}px;padding:{TOP+40}px {R}px 0 {L}px">{lab('Today on our feed')}</div>'''
    cells += frame + pill
    cells += f'''<div class="cell" style="left:0;width:{W}px;height:{H}px;padding:{fy+fh+80}px {R}px {H-BOT}px {L}px">
        <h2 class="h" style="font-size:{88 if len(d["line"]) < 50 else 70}px;line-height:1.04">{d["line"]}</h2>
        <p class="s" style="font-size:52px;margin-top:22px;color:var(--pink)">New on our feed.</p></div>'''
    js = "function draw(){" + skyfill('night') + "CLARI.stars(c,W,H,0.5,{seed:5,n:220,bottom:0.95,alpha:0.8,sparkles:10}); }"
    return wrap(cells, '', js)


FN = {'N': story_N, 'K': story_K, 'W': story_W, 'A': story_A, 'T': story_T}

if __name__ == '__main__':
    only = sys.argv[1:]
    d = os.path.join(S, 'stories'); os.makedirs(d, exist_ok=True)
    jobs, outs = [], []
    for date, t, data in STORIES:
        if only and t not in only and date not in only:
            continue
        hp = os.path.join(d, f'{date}_{t}.html'); open(hp, 'w').write(FN[t](data))
        o = os.path.join(d, f'{date}_{t}.png'); outs.append(o)
        jobs.append(dict(html=hp, w=1080, h=1920, slides=[dict(i=0, out=o)]))
    render('stories', jobs)
    sheet(outs, os.path.join(d, 'sheet_' + ('_'.join(only) if only else 'all') + '.jpg'), cols=min(6, len(outs)), w=300)
