from common import *
import svgkit as K, math

N = 8
TITLE = 'Peri meno post'


def X(fmt, i, u):
    f = FMT[fmt]; return i * f['W'] + f['L'] + u * (f['W'] - f['L'] - f['R'])


def Y(fmt, v):
    f = FMT[fmt]; return f['T'] + v * (f['H'] - f['T'] - f['B'])


def moon(cx, cy, r, phase, uid):
    """moon with soft craters; phase 'wax' lit right, 'wane' lit left, 'full'."""
    o = f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*2.6:.0f}" fill="url(#glowP)"/>'
    o += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="#3A1F66" opacity=".55"/>'  # the unlit disc, faintly visible
    cr = ''.join(f'<circle cx="{cx+r*a:.0f}" cy="{cy+r*b:.0f}" r="{r*s:.0f}" fill="#F0C996" opacity=".22"/>' for a, b, s in [(-.35, -.2, .16), (.2, .35, .12), (.3, -.35, .09), (-.1, .5, .07), (.45, .1, .1)])
    if phase == 'full':
        return o + f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#moonG)"/>' + cr
    off = r * 0.58 if phase == 'wax' else -r * 0.58
    o += (f'<mask id="mk{uid}"><circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r+1:.0f}" fill="#fff"/><circle cx="{cx-off:.0f}" cy="{cy:.0f}" r="{r*0.98:.0f}" fill="#000"/></mask>'
          f'<g mask="url(#mk{uid})"><circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#moonG)"/>{cr}</g>')
    return o


def build_fmt(fmt):
    f = FMT[fmt]; W, H = f['W'], f['H']; PW = W * N
    tall = fmt == 1920
    svg = K.DEFS
    cells = ''
    # orbit: one long arc through every moon, across slides 1 to 4
    big = [(1, 0.80, 0.26, 300, 'wax'), (2, 0.5, 0.24 if not tall else 0.22, 270, 'full'), (3, 0.18, 0.26, 300, 'wane')]
    pts = [(X(fmt, 0, 1.25), Y(fmt, -0.1))] + [(X(fmt, i, u), Y(fmt, v)) for i, u, v, r, p in big] + [(X(fmt, 4, 0.4), Y(fmt, -0.15))]
    d = f'M{pts[0][0]:.0f},{pts[0][1]:.0f}' + ''.join(f' Q{(a[0]+b[0])/2:.0f},{min(a[1],b[1])-160:.0f} {b[0]:.0f},{b[1]:.0f}' for a, b in zip(pts, pts[1:]))
    svg += f'<path d="{d}" fill="none" stroke="#E9DAFF" stroke-opacity=".5" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/>'
    # S1 hook: three rows
    rows = [('wax', 'Perimenopause.'), ('full', 'Menopause.'), ('wane', 'Postmenopause.')]
    rh = 190
    y0 = Y(fmt, 0.02)
    for k, (ph, word) in enumerate(rows):
        cy = y0 + k * rh + 70
        svg += moon(f['L'] + 74, cy, 70, ph, f's1{k}')
        cells += at(0, fmt, f['L'] + 182, cy - 62, f'<p class="h" style="font-size:{108 if not tall else 96}px;line-height:124px;white-space:nowrap">{word}</p>')
    cells += cell(0, fmt, f'<div style="flex:1"></div><h1 class="h" style="font-size:{140 if not tall else 132}px">What\'s the <em>difference?</em></h1>')
    # S2..S4 big moons
    texts = {
        1: ('Perimenopause', 'When your periods become <em>irregular.</em>', None, 'left'),
        2: ('Menopause', 'When you haven\'t had a period for <em>12 months.</em>', 'and you\'re not using hormonal contraception', 'center'),
        3: ('Postmenopause', 'The time <em>after.</em>', 'Some symptoms can carry on, like joint pain and vaginal dryness.', 'right'),
    }
    for (i, u, v, r, ph) in big:
        svg += moon(X(fmt, i, u), Y(fmt, v), r, ph, f'b{i}')
        lab, h, small, al = texts[i]
        hs = 112 if i != 2 else 100
        sm = f'<p class="s" style="font-size:{44 if i == 2 else 56}px;margin-top:28px;text-align:{al};line-height:1.25;{"font-family:Fraunces;font-weight:600" if i==3 else ""}">{small}</p>' if small else ''
        cells += cell(i, fmt, f'''<div style="flex:1"></div>
          <p class="lab" style="font-size:46px;color:var(--pink);text-align:{al}">{lab}</p>
          <h2 class="h" style="font-size:{hs}px;text-align:{al};margin-top:22px">{h}</h2>{sm}''')
    # S5, S6: an age ruler on a shared line
    ly = Y(fmt, 0.38 if not tall else 0.34)
    svg += f'<line x1="{4*W}" x2="{6*W-30}" y1="{ly:.0f}" y2="{ly:.0f}" stroke="#FFF8EC" stroke-opacity=".7" stroke-width="4"/>'
    def ruler(i, a0, a1, hi, marks):
        x0, x1 = i * W + f['L'], i * W + W - f['R']
        o = ''
        px = lambda a: x0 + (a - a0) / (a1 - a0) * (x1 - x0)
        if hi:
            o += f'<rect x="{px(hi[0]):.0f}" y="{ly-46:.0f}" width="{px(hi[1])-px(hi[0]):.0f}" height="92" rx="46" fill="#F7B6CD" opacity=".9"/>'
            o += f'<rect x="{px(hi[0])-30:.0f}" y="{ly-90:.0f}" width="{px(hi[1])-px(hi[0])+60:.0f}" height="180" rx="90" fill="url(#glowP)"/>'
        for a in range(a0, a1 + 1):
            big_ = a % 5 == 0
            o += f'<line x1="{px(a):.0f}" x2="{px(a):.0f}" y1="{ly-(26 if big_ else 12):.0f}" y2="{ly+(26 if big_ else 12):.0f}" stroke="{"#22103F" if hi and hi[0] <= a <= hi[1] else "#FFF8EC"}" stroke-width="{4 if big_ else 3}"/>'
            if big_:
                bold = a in marks or (hi and a in hi)
                cells_ = f'<p class="s" style="font-size:{54 if bold else 42}px;width:120px;text-align:center;opacity:{1 if bold else .7};{"color:var(--pink)" if bold else ""}">{a}</p>'
                yield_ = (px(a) - i * W - 60, ly + 60)
                o += f'<!--lab:{yield_[0]:.0f},{yield_[1]:.0f}-->'
                rl.append(at(i, fmt, yield_[0], yield_[1], cells_))
        for a in marks:
            o += moon(px(a), ly, 30, 'wax', f'r{i}{a}')
        return o
    rl = []
    svg += ruler(4, 40, 60, (45, 55), [])
    svg += ruler(5, 35, 50, None, [40, 45])
    cells += ''.join(rl)
    cells += cell(4, fmt, f'<h2 class="h" style="font-size:{124 if not tall else 112}px;text-align:center">It usually happens between <em style="white-space:nowrap">45 and 55.</em></h2>', pad=(Y(fmt, 0.55), f['B'], f['L'], f['R']))
    cells += cell(5, fmt, f'''<div style="height:{Y(fmt,0.56)-f["T"]:.0f}px"></div>
        <h2 class="h" style="font-size:{84 if not tall else 78}px;text-align:left">Early menopause:<br><em style="font-size:1.3em">before 45.</em></h2>
        <h2 class="h" style="font-size:{84 if not tall else 78}px;text-align:left;margin-top:40px">Premature menopause:<br><em style="font-size:1.3em">before 40.</em></h2>''')
    # S7: no routine test
    svg += moon(X(fmt, 6, 0.82), Y(fmt, 0.08), 90, 'wane', 's7')
    cells += cell(6, fmt, f'''<div style="height:{Y(fmt,0.0)-f["T"]+220:.0f}px"></div>
        <h2 class="h" style="font-size:{96 if not tall else 88}px;color:var(--lilac)">There's no routine test for it.</h2>
        <h2 class="h" style="font-size:{120 if not tall else 106}px;margin-top:50px">A doctor will usually go by your <em>age and symptoms.</em></h2>''')
    # S8 lockup
    lw = 620
    cells += lockup(7, fmt, W / 2, Y(fmt, 0.08 if not tall else 0.16), lw, center=True)
    cells += cell(7, fmt, f'<div style="flex:{1.0 if not tall else 1.35}"></div><h2 class="h" style="font-size:124px;text-align:center">Save this.<br>Send it to <em>her.</em></h2><div style="flex:.5"></div>')
    hb = H - (220 if not tall else 330)
    svg = svg.replace('</defs>', '</defs>' + K.hills(PW, H, hb - 40, 50, seed=2.2, fill='#4A2180', op=.8, waves=(0.0010, 0.0026, 0.0059)) + K.hills(PW, H, hb + 50, 36, seed=5.5, fill='#1C0B36', waves=(0.0012, 0.0029, 0.0071)), 1)
    for k in range(N - 1):
        cells += chrome(k, N, fmt, src='Source: NHS')
    cells += f'<p class="src" style="left:{7*W+f["L"]}px;bottom:{f["sb"]}px">Source: NHS</p>'
    js = f"const BR={H-400 if not tall else H-560};" + """function draw(){ CLARI.sky(c,'night',PW,H,{glow:0});
      for(let i=0;i<N;i++){ const g=c.createRadialGradient(i*W+W*0.5,H*0.3,10,i*W+W*0.5,H*0.3,W); g.addColorStop(0,'rgba(195,168,234,0.10)'); g.addColorStop(1,'rgba(195,168,234,0)'); c.fillStyle=g; c.fillRect(i*W-W,0,W*3,H);}
      CLARI.stars(c,PW,H,0.9,{seed:7,n:1200,bottom:0.88,alpha:0.8,sparkles:28});
      CLARI.branch(c2, 8*W+20, BR, 2.4, true, 0, {blossoms:7});
      CLARI.petal(c, 7*W+300, H*0.30, 1.0, 0.5, 0.8); CLARI.petal(c, 7*W+860, H*0.7, 0.9, -0.6, 0.7); }"""
    return page(TITLE, fmt, N, cells, js=js, svg=svg)


if __name__ == '__main__':
    import sys
    fmts = [int(a) for a in sys.argv[1:]] or [1440, 1920]
    jobs, allouts = [], {}
    for fm in fmts:
        j, outs = build('c5', 'c5', N, fm, build_fmt(fm)); jobs.append(j); allouts[fm] = outs
    render('c5', jobs)
    for fm, outs in allouts.items():
        sheet(outs, f'{S}/c5/sheet_{fm}.jpg')
