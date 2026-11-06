from common import *
import svgkit as K

N = 9
TITLE = "It's not just hot flushes"


def X(fmt, i, u):
    f = FMT[fmt]; return i * f['W'] + f['L'] + u * (f['W'] - f['L'] - f['R'])


def Y(fmt, v):
    f = FMT[fmt]; return f['T'] + v * (f['H'] - f['T'] - f['B'])


def smooth(pts):
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for k in range(1, len(pts)):
        p0 = pts[k - 2] if k > 1 else pts[k - 1]; p1 = pts[k - 1]; p2 = pts[k]; p3 = pts[k + 1] if k + 1 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d


# constellations: slide -> (title html, title placement, stars [(u,v,label,side)], edges)
CONS = {
    2: ('<em>Mind</em>', 'tl', [(0.06, 0.36, 'Mood swings', 'r'), (0.50, 0.25, 'Low mood', 'r'), (0.80, 0.52, 'Anxiety', 'a'),
                              (0.22, 0.74, 'Memory and concentration<br>(brain fog)', 'r')], [(0, 1), (1, 2), (2, 3), (3, 0)]),
    3: ('<em>Sleep</em>', 'br', [(0.10, 0.08, 'Getting to sleep', 'r'), (0.44, 0.30, 'Staying asleep', 'r'),
                               (0.20, 0.56, 'Night sweats', 'r')], [(0, 1), (1, 2)]),
    4: ('<em>Body</em>', 'tr', [(0.06, 0.24, 'Joint aches', 'r'), (0.44, 0.40, 'Muscle pains', 'r'),
                              (0.12, 0.62, 'Headaches and migraines<br>worse than usual', 'r'), (0.60, 0.88, 'Palpitations', 'r')],
        [(0, 1), (1, 2), (2, 3)]),
    5: ('Skin and <em>hair</em>', 'bl', [(0.18, 0.12, 'Dry, itchy skin', 'r'), (0.70, 0.42, 'Hair thinning', 'l')], [(0, 1)]),
}
QUIET = ['Vaginal dryness', 'More UTIs', 'Lower sex drive', 'Sensitive teeth or sore gums']


def build_fmt(fmt):
    f = FMT[fmt]; W, H = f['W'], f['H']; PW = W * N
    svg = K.DEFS
    cells = ''
    trail = []  # chain of star points across all slides
    # --- slide 1: one hot star
    hx, hy = X(fmt, 0, 0.70), Y(fmt, 0.20)
    svg += f'<circle cx="{hx}" cy="{hy}" r="520" fill="url(#glowHot)"/>' + K.sparkle(hx, hy, 150, '#FFF6E2') + f'<circle cx="{hx}" cy="{hy}" r="26" fill="#FFFDF6"/>'
    trail.append((hx, hy)); trail.append((hx, hy))
    cells += cell(0, fmt, f'''<div style="flex:1"></div>
      <h1 class="h" style="font-size:150px;max-width:920px">Hot flushes get all the <em>attention.</em></h1>
      <p class="s" style="font-size:46px;margin-top:44px;display:flex;align-items:center;gap:22px;color:var(--pink)">Swipe for the rest of the NHS list
      <svg width="74" height="30" viewBox="0 0 74 30"><path d="M2 15H68M54 3l14 12-14 12" fill="none" stroke="#F7B6CD" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg></p>''',
                  pad=(f['T'], f['B'] + 20, f['L'], f['R']))
    # --- slide 2: the rest are waiting
    for (u, v, s) in [(0.08, 0.10, 12), (0.30, 0.04, 9), (0.86, 0.12, 14), (0.95, 0.88, 10), (0.12, 0.92, 11), (0.62, 0.95, 8), (0.50, 0.02, 7),
                      (0.70, 0.22, 10), (0.18, 0.24, 8), (0.40, 0.80, 13), (0.80, 0.74, 9), (0.02, 0.62, 10), (0.98, 0.40, 8), (0.58, 0.68, 7)]:
        svg += K.star(X(fmt, 1, u), Y(fmt, v), r=4, glow=30, arms=s * 1.3, op=.9)
    trail.append((X(fmt, 1, 0.30), Y(fmt, 0.04))); trail.append((X(fmt, 1, 0.86), Y(fmt, 0.12)))
    cells += cell(1, fmt, f'<div style="flex:1"></div><h2 class="h" style="font-size:{124 if fmt == 1440 else 112}px;text-align:center">Here\'s what else is on the NHS <em>list.</em></h2><div style="flex:1.15"></div>')
    # --- constellations
    neb = {2: '#B48CF0', 3: '#7F8CF0', 4: '#F28DB2', 5: '#FFC9A0'}
    for i, (title, place, stars, edges) in CONS.items():
        mu = sum(s_[0] for s_ in stars) / len(stars); mv = sum(s_[1] for s_ in stars) / len(stars)
        svg += (f'<radialGradient id="neb{i}"><stop offset="0" stop-color="{neb[i]}" stop-opacity=".30"/><stop offset=".6" stop-color="{neb[i]}" stop-opacity=".08"/><stop offset="1" stop-color="{neb[i]}" stop-opacity="0"/></radialGradient>'
                f'<ellipse cx="{X(fmt, i, mu + 0.12):.0f}" cy="{Y(fmt, mv):.0f}" rx="620" ry="520" fill="url(#neb{i})"/>')
        pts = [(X(fmt, i, u), Y(fmt, v)) for (u, v, _, _) in stars]
        for a, b in edges:
            svg += f'<line x1="{pts[a][0]:.0f}" y1="{pts[a][1]:.0f}" x2="{pts[b][0]:.0f}" y2="{pts[b][1]:.0f}" stroke="#FFF8EC" stroke-opacity=".55" stroke-width="3"/>'
        for (x, y), (u, v, lab, side) in zip(pts, stars):
            svg += K.star(x, y, r=13, glow=80, arms=44)
            maxw = (W - f['R']) - (x - i * W) - 46
            if side == 'r':
                cells += at(i, fmt, x - i * W + 46, y - 30, f'<p class="s" style="font-size:48px;max-width:{maxw:.0f}px">{lab}</p>')
            elif side == 'l':
                cells += at(i, fmt, x - i * W - 46 - 600, y - 30, f'<p class="s" style="font-size:48px;width:600px;text-align:right">{lab}</p>')
            else:
                cells += at(i, fmt, x - i * W - 200, y - 120, f'<p class="s" style="font-size:48px;width:400px;text-align:center">{lab}</p>')
        trail.append(min(pts)); trail.append(max(pts))
        al = {'tl': ('flex-start', 'left', 0), 'tr': ('flex-end', 'right', 0), 'bl': ('flex-start', 'left', 1), 'br': ('flex-end', 'right', 1)}[place]
        h = f'<h2 class="h" style="font-size:{172 if len(title) < 16 else 150}px;text-align:{al[1]}">{title}</h2>'
        cells += cell(i, fmt, (f'<div style="flex:1"></div>{h}' if al[2] else f'{h}<div style="flex:1"></div>'),
                      pad=(f['T'] - 20, f['B'] - 10, f['L'], f['R']))
    # --- slide 7: the quiet ones (dashed, dimmer)
    qy = [0.40, 0.55, 0.70, 0.85]
    qp = [(X(fmt, 6, 0.02 + (0.03 if k % 2 else 0)), Y(fmt, v)) for k, v in enumerate(qy)]
    for a in range(3):
        svg += f'<line x1="{qp[a][0]:.0f}" y1="{qp[a][1]:.0f}" x2="{qp[a+1][0]:.0f}" y2="{qp[a+1][1]:.0f}" stroke="#F7B6CD" stroke-opacity=".7" stroke-width="3" stroke-dasharray="3 14" stroke-linecap="round"/>'
    for (x, y), lab in zip(qp, QUIET):
        svg += K.star(x, y, r=8, glow=44, arms=22, op=.9)
        cells += at(6, fmt, x - 6 * W + 44, y - 30, f'<p class="s" style="font-size:48px">{lab}</p>')
    trail.append(qp[0]); trail.append(None)
    cells += cell(6, fmt, '<h2 class="h" style="font-size:112px;text-align:right;max-width:880px;align-self:flex-end">The ones people don\'t say <em>out loud.</em></h2><div style="flex:1"></div>')
    # --- slide 8: a cycle ring, the spacing changes
    cx, cy, R = X(fmt, 7, 0.5), Y(fmt, 0.24 if fmt == 1440 else 0.20), (250 if fmt == 1440 else 210)
    import math
    ang = []
    a = -90.0
    for k in range(28):
        ang.append(a)
        step = 360 / 28 if k < 14 else (360 / 28) * (0.55 if k % 3 == 0 else 1.25)
        a += step
    for k, d in enumerate(ang):
        r = math.radians(d)
        big = k in (0, 1, 2, 3, 4)
        svg += f'<circle cx="{cx+R*math.cos(r):.1f}" cy="{cy+R*math.sin(r):.1f}" r="{13 if big else 9}" fill="{"#F7B6CD" if big else "#FFF8EC"}" opacity="{1 if big else .75}"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="{R*2.0}" fill="url(#glowP)" opacity=".7"/>'
    trail.append(None); trail.append((cx + R, cy))
    cells += cell(7, fmt, f'<div style="flex:1.25"></div><h2 class="h" style="font-size:{108 if fmt == 1440 else 98}px;text-align:center">One of the first signs is usually a <em>change</em> to your periods.</h2><div style="flex:.25"></div>')
    # --- slide 9: lockup
    lw = 640
    ly = Y(fmt, 0.18)
    cells += lockup(8, fmt, W / 2, ly, lw, center=True)
    trail.append((8 * W + W / 2 - lw * 0.28, ly + lw * 0.22)); trail.append(trail[-1])
    cells += cell(8, fmt, '<div style="flex:1.5"></div><h2 class="h" style="font-size:120px;text-align:center">Save this.<br>Send it to <em>her.</em></h2><div style="flex:.4"></div>')
    # trail: dotted links between constellations (drawn under stars)
    links = ''
    for k in range(1, len(trail) - 1, 2):
        if trail[k] is None or trail[k + 1] is None: continue
        (x1, y1), (x2, y2) = trail[k], trail[k + 1]
        if abs(x1 - x2) < 1 and abs(y1 - y2) < 1: continue
        links += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"/>'
    svg = svg.replace('</defs>', '</defs>' + f'<g stroke="#E9DAFF" stroke-opacity=".62" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round">{links}</g>', 1)
    # horizon
    hb = H - (230 if fmt == 1440 else 330)
    svg += ('<linearGradient id="hb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6A39A8"/><stop offset="1" stop-color="#3A1A68"/></linearGradient>'
            '<linearGradient id="hf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E1458"/><stop offset="1" stop-color="#1A0A33"/></linearGradient>')
    hills = K.hills(PW, H, hb - 60, 70, seed=1.3, fill='url(#hb)', op=.9, waves=(0.0009, 0.0023, 0.0061)) + K.hills(PW, H, hb + 50, 48, seed=4.1, fill='url(#hf)', op=1, waves=(0.0013, 0.0031, 0.0077))
    svg = svg.replace('</defs>', '</defs>' + hills, 1)
    # chrome
    for i in range(N - 1):
        cells += chrome(i, N, fmt, src='Source: NHS')
    cells += chrome(8, N, fmt, src='Source: NHS', counter=False).split('>', 1)[1]  # drop the mark on the lockup slide
    js = f'const RX={cx},RY={cy};' + """function draw(){ CLARI.sky(c,'night',PW,H,{glow:0});
      for(let i=0;i<N;i++){ const g=c.createRadialGradient(i*W+W*0.7,H*0.18,10,i*W+W*0.7,H*0.18,W*0.9); g.addColorStop(0,'rgba(249,201,216,0.10)'); g.addColorStop(1,'rgba(249,201,216,0)'); c.fillStyle=g; c.fillRect(i*W-W,0,W*3,H);}
      CLARI.stars(c,PW,H,0.4,{seed:11,n:1100,bottom:0.9,alpha:0.75,sparkles:30});
      CLARI.branch(c, 9*W+40, -30, 2.6, true, 0, {blossoms:7});
      CLARI.moon(c, RX, RY, 78, {glow:0.6});
      CLARI.petal(c, 8*W+170, H*0.42, 1.0, 0.7, 0.85); CLARI.petal(c, 8*W+900, H*0.62, 0.8, -0.4, 0.75); }"""
    return page(TITLE, fmt, N, cells, js=js, svg=svg)


if __name__ == '__main__':
    import sys
    fmts = [int(a) for a in sys.argv[1:]] or [1440, 1920]
    jobs, allouts = [], {}
    for fm in fmts:
        j, outs = build('c1', 'c1', N, fm, build_fmt(fm)); jobs.append(j); allouts[fm] = outs
    render('c1', jobs)
    for fm, outs in allouts.items():
        sheet(outs, f'{S}/c1/sheet_{fm}.jpg')
