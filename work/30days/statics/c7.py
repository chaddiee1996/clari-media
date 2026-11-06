from common import *
import svgkit as K, math, re

N = 7
TITLE = 'When to contact your GP'
CSS = """
body{background:#FBF6EE}
.h{color:#241A33} .h em{color:#B83A68}
.no{font-family:'Figtree',sans-serif;font-weight:800;color:#B83A68;margin:0;letter-spacing:.06em}
"""
ITEMS = [
    (1, 'You think it could be perimenopause or menopause, and want to know your <em>options.</em>', 'left'),
    (2, 'Symptoms like a fast heartbeat <em>(palpitations).</em>', 'right'),
    (3, 'You still have periods, but you\'re bleeding <em>more,</em> not less, than before.', 'left'),
    (4, 'You haven\'t had a period for 12 months or more, and then get <em>any</em> vaginal bleeding.', 'right'),
]


def build_fmt(fmt):
    f = FMT[fmt]; W, H = f['W'], f['H']; PW = W * N
    tall = fmt == 1920
    svg = K.DEFS
    cells = ''
    svg += f'<rect width="{PW}" height="{H}" fill="#FBF6EE"/>'
    for x in range(0, PW, 60):
        svg += f'<line x1="{x}" x2="{x}" y1="0" y2="{H}" stroke="#EFE6D8" stroke-width="2"/>'
    for y in range(0, H, 60):
        svg += f'<line x1="0" x2="{PW}" y1="{y}" y2="{y}" stroke="#EFE6D8" stroke-width="2"/>'
    # header band, continuous: like the app's GP summary header
    bt = f['ct'] - 30
    bh = 146
    svg += f'<rect x="0" y="{bt}" width="{PW}" height="{bh}" fill="#4A2070"/><rect x="0" y="{bt+bh}" width="{PW}" height="8" fill="#F7B6CD"/>'
    for i in range(N - 1):
        cells += (f'<p class="lab abs" style="left:{i*W+f["L"]+110}px;top:{bt+50}px;font-size:40px;color:#F7B6CD;letter-spacing:.16em">'
                  f'{"NHS advice" if i else "NHS advice"}</p>')
    T = bt + bh + 90
    # S1 hook
    cells += cell(0, fmt, f'''<div style="height:{(30 if not tall else 50)}px"></div>
      <h1 class="h" style="font-size:{132 if not tall else 128}px;line-height:1.0">When the NHS says to <em>contact your GP.</em></h1>''', pad=(T, f['B'], f['L'], f['R']))
    # items: number + drawing share the top row, the headline sits on the stethoscope line
    ty = H - (300 if not tall else 360)
    TB = H - (ty - (120 if not tall else 205))
    pen = 'fill="none" stroke="#4A2070" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"'
    ic_y = T + (120 if not tall else 200)
    penf = lambda fill: f'fill="{fill}" stroke="#4A2070" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"'
    def plain(t): return re.sub('<[^>]+>', '', t)
    for (n, text, al) in ITEMS:
        i = n
        ln = len(plain(text))
        fs = (128 if ln < 50 else (108 if ln < 75 else (100 if ln < 90 else 94))) - (8 if tall else 0)
        cells += cell(i, fmt, f'''
          <div style="display:flex;align-items:center;gap:34px;flex-direction:{'row' if al=='left' else 'row-reverse'}">
            <div style="width:150px;height:150px;border-radius:40px;border:8px solid #4A2070;box-sizing:border-box;flex-shrink:0;background:#fff"></div>
            <p class="no" style="font-size:190px;font-family:Fraunces;font-weight:800;letter-spacing:-.02em;color:#F3AFC8;line-height:.8">{n}</p>
          </div>
          <div style="flex:1"></div>
          <h2 class="h" style="font-size:{fs}px;text-align:{al}">{text}</h2>''', pad=(T, TB, f['L'], f['R']))
    side = lambda i, al: i * W + (W * 0.70 if al == 'left' else W * 0.30)
    icx = {n: side(n, al) for (n, _, al) in ITEMS}
    icons = {
        1: f'<g transform="translate({icx[1]},{ic_y}) scale(1.1)"><path {penf("#FFFFFF")} d="M-140 -90 H140 Q170 -90 170 -60 V40 Q170 70 140 70 H-40 L-100 120 L-90 70 H-140 Q-170 70 -170 40 V-60 Q-170 -90 -140 -90Z"/><circle cx="-70" cy="-10" r="14" fill="#B83A68"/><circle cx="0" cy="-10" r="14" fill="#B83A68"/><circle cx="70" cy="-10" r="14" fill="#B83A68"/></g>',
        2: f'<g transform="translate({icx[2]},{ic_y+60}) scale(.85)"><path d="M0 120 C-90 60 -210 -10 -210 -100 C-210 -160 -160 -200 -105 -200 C-60 -200 -20 -170 0 -135 C20 -170 60 -200 105 -200 C160 -200 210 -160 210 -100 C210 -10 90 60 0 120Z" fill="#FCE3EC"/>'
           f'<polyline points="-250,-40 -110,-40 -80,-40 -50,-150 -10,90 30,-90 60,-40 250,-40" fill="none" stroke="#E8628F" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>',
        3: f'<g transform="translate({icx[3]},{ic_y+20}) scale(1.15)"><path d="M-60 -120 C-60 -120 -130 -30 -130 20 A70 70 0 0 0 10 20 C10 -30 -60 -120 -60 -120Z" fill="#F7B6CD"/><path d="M60 -170 C60 -170 160 -40 160 30 A100 100 0 0 1 -40 30 C-40 -40 60 -170 60 -170Z" fill="none" stroke="#B83A68" stroke-width="8"/></g>',
        4: f'<g transform="translate({icx[4]+8},{ic_y-60}) scale(1.0)">' + ''.join(f'<rect x="{-180+c_*96}" y="{-60+r_*76}" width="76" height="60" rx="12" {pen if not (r_==2 and c_==3) else "fill=\"#F7B6CD\" stroke=\"#4A2070\" stroke-width=\"8\""}/>' for r_ in range(3) for c_ in range(4)) + '</g>',
        5: f'<g transform="translate({5*W+W*0.5},{ic_y})">'
           f'<g transform="translate(-280,0)"><path {penf("#FCE3EC")} d="M0 100 C-60 60 -120 20 -120 -40 C-120 -80 -90 -105 -55 -105 C-28 -105 -10 -88 0 -70 C10 -88 28 -105 55 -105 C90 -105 120 -80 120 -40 C120 20 60 60 0 100Z"/></g>'
           f'<g><circle cx="-38" cy="0" r="70" {pen}/><circle cx="38" cy="0" r="70" fill="none" stroke="#E8628F" stroke-width="8"/></g>'
           f'<g transform="translate(280,0)"><path {pen} d="M-110 -50 Q-112 90 -106 100 Q0 106 106 100 Q112 50 110 -50 Q0 -56 -110 -50Z M-40 -52 Q-40 -96 0 -96 Q40 -96 40 -52 M-110 10 Q0 24 110 8"/></g></g>',
    }
    for k_, ic in icons.items():
        svg += ic
    # S6
    cells += cell(5, fmt, f'''<div style="flex:1"></div><h2 class="h" style="font-size:{96 if not tall else 96}px;text-align:center">Early advice can help reduce the effects on your <em>health, relationships and work.</em></h2>''', pad=(T + 260, TB, f['L'], f['R']))
    # S7 lockup
    cells += lockup(6, fmt, W / 2, T + 40, 640, dark=True, center=True)
    cells += cell(6, fmt, f'<div style="height:{640*0.44+120}px"></div><h2 class="h" style="font-size:150px;text-align:center"><em>Save</em> this.</h2>', pad=(T, f['B'], f['L'], f['R']))
    # the stethoscope: one tube winding through every slide
    ty = H - (300 if not tall else 360)
    pts = [(0.62 * W, ty - 70), (0.72 * W, ty + 20), (0.8 * W, ty + 10), (1.3 * W, ty + 20), (2.0 * W, ty - 50), (2.7 * W, ty + 30),
           (3.4 * W, ty - 40), (4.1 * W, ty + 30), (4.8 * W, ty - 40), (5.5 * W, ty + 20), (6.2 * W, ty - 10), (6.72 * W, ty - 70)]
    d = f'M{pts[0][0]:.0f},{pts[0][1]:.0f}'
    for k in range(1, len(pts)):
        p0 = pts[k - 2] if k > 1 else pts[k - 1]; p1 = pts[k - 1]; p2 = pts[k]; p3 = pts[k + 1] if k + 1 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6); c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.0f},{c1[1]:.0f} {c2[0]:.0f},{c2[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}'
    svg += f'<path d="{d}" fill="none" stroke="#2A1548" stroke-opacity=".18" stroke-width="30" stroke-linecap="round" transform="translate(0,14)"/>'
    svg += f'<path d="{d}" fill="none" stroke="#7A45B5" stroke-width="26" stroke-linecap="round"/>'
    svg += f'<path d="{d}" fill="none" stroke="#B48CF0" stroke-width="7" stroke-linecap="round" transform="translate(-3,-6)" opacity=".8"/>'
    # earpieces (S1) at the start of the tube
    ex, ey = pts[0]
    svg += (f'<g transform="translate({ex},{ey}) scale(.8)">'
            f'<path d="M0 0 C-20 -120 -170 -170 -190 -400 M0 0 C20 -120 170 -170 190 -400" fill="none" stroke="#2A1548" stroke-opacity=".15" stroke-width="24" stroke-linecap="round" transform="translate(0,12)"/>'
            f'<path d="M0 0 C-20 -120 -170 -170 -190 -400 M0 0 C20 -120 170 -170 190 -400" fill="none" stroke="#C9BFD6" stroke-width="20" stroke-linecap="round"/>'
            f'<path d="M-4 -10 C-24 -120 -166 -176 -186 -396 M4 -10 C24 -120 166 -176 186 -396" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".7"/>'
            f'<path d="M-190 -400 C-200 -440 -150 -460 -120 -440" fill="none" stroke="#C9BFD6" stroke-width="18" stroke-linecap="round"/><path d="M190 -400 C200 -440 150 -460 120 -440" fill="none" stroke="#C9BFD6" stroke-width="18" stroke-linecap="round"/>'
            f'<ellipse cx="-112" cy="-440" rx="26" ry="20" fill="#E8628F"/><ellipse cx="112" cy="-440" rx="26" ry="20" fill="#E8628F"/>'
            f'<circle cx="0" cy="0" r="28" fill="#C9BFD6"/></g>')
    # chest piece (S7)
    cx, cy = pts[-1]
    svg += (f'<g transform="translate({cx},{cy - 60})" filter="url(#soft)"><rect x="-14" y="30" width="28" height="60" rx="10" fill="#C0B5CC"/>'
            f'<circle r="92" fill="#D8D0E2"/><circle r="72" fill="#F4EFF8"/><circle r="72" fill="none" stroke="#B3A8BF" stroke-width="6"/></g>')
    if True:
        # chest piece sits at bottom of the lockup slide; keep it away from the text
        pass
    for k in range(N - 1):
        cells += chrome(k, N, fmt, src='Source: NHS', mark='mark.png', ct=bt + 30)
    cells = cells.replace('class="counter"', 'class="counter" data-x="1"')
    css = CSS + '.counter{color:#FFF8EC!important}'
    return page(TITLE, fmt, N, cells, svg=svg, css=css, light=True, bg='#FBF6EE')


if __name__ == '__main__':
    import sys
    fmts = [int(a) for a in sys.argv[1:]] or [1440, 1920]
    jobs, allouts = [], {}
    for fm in fmts:
        j, outs = build('c7', 'c7', N, fm, build_fmt(fm)); jobs.append(j); allouts[fm] = outs
    render('c7', jobs)
    for fm, outs in allouts.items():
        sheet(outs, f'{S}/c7/sheet_{fm}.jpg')
