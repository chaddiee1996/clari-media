from common import *
import svgkit as K, math, json

N = 8
TITLE = 'What to say to a friend'
CSS = """
.card{position:absolute;width:940px;height:740px;border-radius:14px;background:linear-gradient(160deg,#FFFDF7,#F6EEE2);box-shadow:0 30px 60px rgba(16,4,40,.45);box-sizing:border-box;padding:56px 0 0 58px}
.card .k{font-family:'Figtree',sans-serif;font-weight:800;font-size:40px;letter-spacing:.18em;text-transform:uppercase;color:#B83A68;margin:0}
.card .was{font-family:'Caveat',cursive;font-weight:700;font-size:96px;color:#6B5A7E;margin:0;line-height:1.0;text-decoration:line-through;text-decoration-color:#B83A68;text-decoration-thickness:7px}
.card .try{font-family:'Fraunces',serif;font-weight:700;font-variation-settings:"opsz" 144;font-size:88px;line-height:1.04;color:#241A33;margin:8px 0 0;letter-spacing:-.01em;word-spacing:.04em}
.card .try em{font-style:italic;font-weight:600;color:#B83A68}
.stamp{position:absolute;right:46px;top:46px;width:170px;height:206px;background:#fff;padding:14px;box-sizing:border-box;box-shadow:0 3px 8px rgba(34,16,63,.18);
 outline:7px dotted #F6EEE2;outline-offset:-3px}
"""
CARDS = [
    (1, 'You look fine!', 'How are you <em>really</em> sleeping?', 'night'),
    (2, "It's just your age.", "That sounds hard. What's it <em>like?</em>", 'evening'),
    (3, 'Have you tried yoga?', 'Do you want ideas, or just a <em>moan?</em>', 'dawn'),
    (4, "I'm sure it's nothing.", "Have you told your GP? I'll come <em>with you.</em>", 'day'),
    (5, 'Cheer up.', "You're not <em>imagining</em> it.", 'icon'),
]
SKYC = {'night': ('#2C1252', '#8E57BE'), 'evening': ('#391766', '#F7B9CB'), 'dawn': ('#7A52B4', '#FFDDB5'), 'day': ('#9A90E2', '#FBE0EC'), 'icon': ('#7A45B5', '#22103F')}


def mug(col, col2, flip=False, s=1):
    sx = -1 if flip else 1
    return (f'<g transform="scale({sx*s},{s})">'
            f'<path d="M96 -200 C175 -200 175 -80 96 -80" fill="none" stroke="{col2}" stroke-width="28"/>'
            f'<path d="M-110 -260 L110 -260 L100 -20 Q98 0 76 0 L-76 0 Q-98 0 -100 -20Z" fill="{col}"/>'
            f'<path d="M-80 -230 L-74 -40" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity=".25"/>'
            f'<ellipse cx="0" cy="-260" rx="110" ry="22" fill="{col2}"/><ellipse cx="0" cy="-258" rx="94" ry="15" fill="#6E4334"/></g>')


def steam(x, y, s=1, op=.75):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="#FFF8EC" stroke-width="10" stroke-linecap="round" opacity="{op}">'
            '<path d="M-30 0 C-70 -50 10 -80 -30 -140 C-60 -180 -10 -210 -30 -250"/><path d="M30 -10 C0 -60 70 -90 30 -150"/></g>')


def build_fmt(fmt):
    f = FMT[fmt]; W, H = f['W'], f['H']; PW = W * N
    sill = 1210
    svg = K.DEFS
    cells = ''
    # fairy lights: catenaries hooked at slide centres, so every wire crosses a slide edge
    lights = ''
    for i in range(N):
        x0, x1 = i * W + W * 0.5, (i + 1) * W + W * 0.5
        sag = 120
        pts = [(x0 + (x1 - x0) * t, 150 + sag * 4 * t * (1 - t)) for t in [k / 40 for k in range(41)]]
        lights += f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="none" stroke="#1A0B30" stroke-width="3" opacity=".8"/>'
        for k in range(1, 9):
            t = k / 9; x = x0 + (x1 - x0) * t; y = 150 + sag * 4 * t * (1 - t) + 14
            colr = ['#FFE29A', '#F7B6CD', '#FFF3D0'][k % 3]
            lights += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="34" fill="url(#glowW)" opacity=".8"/><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="9" ry="13" fill="{colr}"/>'
    # sill + wall below
    svg += (f'<rect x="0" y="{sill}" width="{PW}" height="{H-sill}" fill="#2A1548"/>'
            f'<rect x="0" y="{sill-30}" width="{PW}" height="46" rx="6" fill="#4A2A72"/><rect x="0" y="{sill-30}" width="{PW}" height="8" fill="#6B4796"/>'
            f'<rect x="0" y="{sill+16}" width="{PW}" height="20" fill="#1C0C36" opacity=".6"/>')
    svg += lights
    # S1 two mugs
    svg += f'<g transform="translate({W*0.32},{sill-28})" filter="url(#soft)">{mug("#F28DB2", "#E8628F")}</g>' + steam(W * 0.32, sill - 300, .6)
    svg += f'<g transform="translate({W*0.70},{sill-28})" filter="url(#soft)">{mug("#B48CF0", "#7A45B5", True)}</g>' + steam(W * 0.70, sill - 300, .55)
    cells += cell(0, fmt, '<h1 class="h" style="font-size:118px;text-align:center">What to say to a friend who\'s struggling with <em>perimenopause.</em></h1>', pad=(250, 0, f['L'], f['R']))
    # postcards
    for k, (i, was, try_, sky) in enumerate(CARDS):
        rot = [-2.2, 1.8, -1.6, 2.4, -2.0][k]
        top = 330
        a, b = SKYC[sky]
        stamp = (f'<div class="stamp"><div style="width:100%;height:100%;background:linear-gradient(180deg,{a},{b});display:flex;align-items:center;justify-content:center">'
                 f'<img src="../assets/mark.png" style="width:96px"></div></div>')
        pm = ('<svg style="position:absolute;right:16px;top:272px" width="260" height="130" viewBox="0 0 260 130">'
              '<circle cx="80" cy="64" r="56" fill="none" stroke="#7A45B5" stroke-width="4" opacity=".55"/><circle cx="80" cy="64" r="42" fill="none" stroke="#7A45B5" stroke-width="3" opacity=".4"/>'
              + ''.join(f'<path d="M130 {30+j*22} C160 {18+j*22} 190 {42+j*22} 255 {30+j*22}" fill="none" stroke="#7A45B5" stroke-width="4" opacity=".5"/>' for j in range(4)) + '</svg>')
        addr = ''.join(f'<div style="position:absolute;right:46px;width:230px;top:{450+j*80}px;height:3px;background:#CDBFDC"></div>' for j in range(3))
        cells += (f'<div class="card" style="left:{i*W+70}px;top:{top}px;transform:rotate({rot}deg)">'
                  f'{stamp}{pm}{addr}<div style="position:absolute;left:640px;top:300px;bottom:60px;width:3px;background:#E2D6EA"></div>'
                  f'<div style="width:560px"><p class="k">Instead of</p><p class="was">{was}</p>'
                  f'<p class="k" style="margin-top:44px">Try</p><p class="try">{try_}</p></div>'
                  f'<div style="position:absolute;left:{360+k*40}px;top:-26px;width:190px;height:54px;background:rgba(247,182,205,.75);transform:rotate({-rot*1.5}deg)"></div></div>')
    # S7 the NHS line, mugs together
    svg += f'<g transform="translate({6*W+W*0.40},{sill-28})" filter="url(#soft)">{mug("#F28DB2", "#E8628F", False, .8)}</g>'
    svg += f'<g transform="translate({6*W+W*0.64},{sill-28})" filter="url(#soft)">{mug("#B48CF0", "#7A45B5", True, .8)}</g>'
    svg += steam(6 * W + W * 0.52, sill - 240, .7)
    cells += cell(6, fmt, '<h2 class="h" style="font-size:104px;text-align:left">The NHS suggests talking to people going through the <em>same thing.</em></h2>', pad=(270, 0, f['L'], f['R']))
    # S8 postcard front with the lockup
    cells += (f'<div class="card" style="left:{7*W+70}px;top:330px;transform:rotate(1.6deg);background:linear-gradient(160deg,#4A2070,#22103F);padding:0;display:flex;flex-direction:column;align-items:center;justify-content:center">'
              f'<img src="../assets/lockup-light.png" style="width:560px;margin-bottom:40px"><h2 class="h" style="font-size:120px;text-align:center">Send this to <em>her.</em></h2>'
              f'<div style="position:absolute;left:380px;top:-26px;width:190px;height:54px;background:rgba(247,182,205,.75);transform:rotate(-3deg)"></div></div>')
    for k in range(N - 1):
        cells += chrome(k, N, fmt, src=('Source: NHS' if k == 6 else None))
    js = """function draw(){ CLARI.sky(c,'evening',PW,H,{glow:0});
      for(let i=0;i<N;i++){ const g=c.createRadialGradient(i*W+W*0.5,H*0.7,10,i*W+W*0.5,H*0.7,W*0.9); g.addColorStop(0,'rgba(255,214,190,0.18)'); g.addColorStop(1,'rgba(255,214,190,0)'); c.fillStyle=g; c.fillRect(i*W-W,0,W*3,H);}
      CLARI.stars(c,PW,H,0.6,{seed:31,n:900,bottom:0.5,alpha:0.7,sparkles:20});
      CLARI.moon(c, W*0.88, 800, 62, {glow:1});
      CLARI.hills(c, PW, 1210, 'evening', {y:0});
      CLARI.branch(c2, 4*W+60, 1210-110, 2.4, true, 0, {blossoms:7});
      CLARI.branch(c2, 4*W-60, 1210-110, 2.2, false, 0, {blossoms:6});
    }"""
    return page(TITLE, fmt, N, cells, js=js, svg=svg, css=CSS)


if __name__ == '__main__':
    j, outs = build('c8', 'c8', N, 1440, build_fmt(1440))
    render('c8', [j]); sheet(outs, f'{S}/c8/sheet_1440.jpg')
