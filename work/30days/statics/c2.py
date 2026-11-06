from common import *
import svgkit as K, math

N = 8
TITLE = 'Before your GP appointment'
INK = '#241A33'; PEN = '#4A2070'; ROSE = '#B83A68'; NUM = '#F3AFC8'

CSS = """
body{background:#FBF6EE}
.h{color:#241A33}
.pen{font-family:'Caveat',cursive;font-weight:700;color:#4A2070;line-height:96px;margin:0}
.num{font-family:'Fraunces',serif;font-style:italic;font-weight:600;font-variation-settings:"opsz" 144;color:#F3AFC8;line-height:.8;margin:0;position:absolute}
"""


def wobble_line(x1, y, x2, amp=5, seed=0, w=7, col=ROSE, op=1):
    pts = []
    n = int((x2 - x1) / 40) + 2
    for k in range(n + 1):
        x = x1 + (x2 - x1) * k / n
        pts.append(f'{x:.0f},{y + amp*math.sin(k*1.7+seed) + (k/n)*-6:.1f}')
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'


def hand_circle(cx, cy, rx, ry, col=ROSE, w=5, seed=0):
    # two slightly offset loops, like a pen circling a word
    d = ''
    for loop in range(2):
        pts = []
        for k in range(0, 41):
            a = -2.2 + k / 40 * (math.tau + 0.5)
            r1 = 1 + 0.04 * math.sin(a * 3 + seed + loop)
            pts.append(f'{cx + rx*r1*math.cos(a) + loop*6:.1f},{cy + ry*r1*math.sin(a) - loop*4:.1f}')
        d += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{w - loop*2}" stroke-linecap="round" opacity="{1 - loop*0.35}"/>'
    return d


def tick_box(x, y, s=70):
    return (f'<path d="M{x+4},{y+6} Q{x+s/2},{y-2} {x+s-2},{y+4} Q{x+s+3},{y+s/2} {x+s-4},{y+s-2} Q{x+s/2},{y+s+4} {x+3},{y+s-3} Q{x-3},{y+s/2} {x+4},{y+6}Z" '
            f'fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M{x+14},{y+s*0.52} L{x+s*0.42},{y+s*0.8} L{x+s+18},{y-14}" fill="none" stroke="{ROSE}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')


def pencil(x, y, L, rot):
    w = 58
    return (f'<g transform="translate({x},{y}) rotate({rot})" filter="url(#softS)">'
            f'<rect x="0" y="0" width="{L}" height="{w}" rx="6" fill="#C3A8EA"/>'
            f'<rect x="0" y="{w*0.36}" width="{L}" height="{w*0.28}" fill="#B096DC"/>'
            f'<rect x="0" y="0" width="{L}" height="{w*0.12}" fill="#D9C8F2"/>'
            f'<rect x="{L}" y="0" width="56" height="{w}" fill="#CFC6D8"/><rect x="{L+12}" y="0" width="6" height="{w}" fill="#B3A8BF"/><rect x="{L+34}" y="0" width="6" height="{w}" fill="#B3A8BF"/>'
            f'<rect x="{L+56}" y="0" width="70" height="{w}" rx="16" fill="#F28DB2"/>'
            f'<path d="M0,0 L-130,{w/2} L0,{w} Z" fill="#F3D9B5"/><path d="M-92,{w*0.35} L-130,{w/2} L-92,{w*0.65} Z" fill="{INK}"/>'
            f'</g>')


def spiral(pw):
    o = ''
    for x in range(30, pw, 60):
        o += (f'<circle cx="{x}" cy="58" r="11" fill="#E5DCCD"/>'
              f'<rect x="{x-6}" y="-12" width="12" height="74" rx="6" fill="#7E7290"/>'
              f'<rect x="{x-6}" y="-12" width="5" height="70" rx="3" fill="#B7ADC4"/>')
    return o


def build_fmt(fmt):
    f = FMT[fmt]; W, H = f['W'], f['H']; PW = W * N
    L = f['L']
    svg = K.DEFS
    # paper + rules (continuous across every slide)
    svg += f'<rect width="{PW}" height="{H}" fill="#FBF6EE"/>'
    svg += f'<rect width="{PW}" height="96" fill="#F1E9DC"/>'
    svg += f'<line x1="0" x2="{PW}" y1="206" y2="206" stroke="#E7A9C0" stroke-width="3"/><line x1="0" x2="{PW}" y1="214" y2="214" stroke="#E7A9C0" stroke-width="3"/>'
    for y in range(310, H - 60, 96):
        svg += f'<line x1="0" x2="{PW}" y1="{y}" y2="{y}" stroke="#D9CCEB" stroke-width="2.5"/>'
    rule = lambda k: 310 + 96 * k   # y of ruled line k
    svg += spiral(PW)
    cells = ''
    # objects that cross slide edges
    svg += pencil(W * 0.62, 330, 760, -11)                                  # S1 -> S2
    svg += f'<circle cx="{W*4}" cy="{rule(10)+20}" r="150" fill="none" stroke="#C79A6B" stroke-opacity=".16" stroke-width="16" stroke-dasharray="520 60 200 90"/>'  # mug ring S4|S5
    svg += K.blossom(W * 6 + 6, rule(11) - 10, 2.0, 14, op=.9) + K.petal(W * 6 + 160, rule(12) - 30, 1.3, 70, .8)  # pressed blossom S6|S7
    svg += K.petal(W * 1 - 120, H - 150, 1.1, -30, .7)

    # S1 hook
    cells += at(0, fmt, L, rule(5) - 70, f'<h1 class="h" style="font-size:136px;width:920px;line-height:1.0">Before your GP appointment, <em style="white-space:nowrap">write these down.</em></h1>')
    svg += wobble_line(L + 4, rule(5) - 70 + 136 * 2 + 158, L + 880, amp=4, seed=1.2, w=8)
    # S2..S7 items
    items = [
        # (slide, numeral side, prompt, example lines, align)
        (1, 'l', "What's changed, and when it started.", ["Waking at 3am since August"], 'left'),
        (2, 'r', 'How often, and how bad.', ['Most nights.', 'Bad enough to change the sheets.'], 'right'),
        (4, 'l', 'What seems to set it off.', ['Wine.', 'Hot rooms.', 'Stress at work.'], 'left'),
        (5, 'r', "How it's affecting work, sleep and the people around you.", [], 'right'),
    ]
    for (i, side, prompt, ex, al) in items:
        n = i
        nx = L - 20 if side == 'l' else W - f['R'] - 300
        cells += f'<p class="num" style="left:{i*W+nx}px;top:{236}px;font-size:340px;{"text-align:right;width:320px" if side=="r" else ""}">{n}</p>'
        cells += at(i, fmt, L, rule(2) + 40, f'<h2 class="h" style="font-size:{100 if len(prompt) < 25 else 92}px;width:{W-L-f["R"]}px;text-align:{al}">{prompt}</h2>')
        bx = L + 6 if al == 'left' else W - f['R'] - 76
        svg += tick_box(i * W + bx, 236 + 30, 72) if False else ''
        for k, line in enumerate(ex):
            yy = rule(6 + k) - 78
            cells += at(i, fmt, L, yy, f'<p class="pen" style="font-size:86px;width:{W-L-f["R"]}px;text-align:{al}">{line}</p>')
    # S4 periods: options circled
    i = 3
    cells += f'<p class="num" style="left:{i*W+W/2-100}px;top:236px;font-size:340px;width:200px;text-align:center">3</p>'
    cells += at(i, fmt, L, rule(2) + 40, f'<h2 class="h" style="font-size:112px;width:{W-2*L}px;text-align:center">Your periods:</h2>')
    opts = [('more often,', 0.27, 5), ('less often,', 0.73, 5), ('heavier,', 0.27, 8), ('lighter.', 0.73, 8)]
    for k, (t, u, r) in enumerate(opts):
        x = W * u
        cells += at(i, fmt, x - 230, rule(r) - 78, f'<p class="pen" style="font-size:92px;width:460px;text-align:center">{t}</p>')
        svg += hand_circle(i * W + x, rule(r) - 34, 200, 70, seed=k * 1.3, col=PEN if k % 2 else ROSE, w=5)
    # S6 doodles: work, sleep, people around you (pen lines)
    dx = 5 * W + W - f['R']
    dy = rule(6) + 40
    pen = f'fill="none" stroke="{PEN}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"'
    svg += (f'<g transform="translate({dx-760},{dy-40}) rotate(-4)"><path {pen} d="M10 40 Q8 120 14 150 Q90 156 170 148 Q176 100 172 40 Q90 34 10 40Z M60 40 Q60 12 90 12 Q120 12 122 40 M12 84 Q90 96 172 82"/></g>'
            f'<g transform="translate({dx-470},{dy-50}) rotate(3)"><path {pen} d="M70 10 A70 70 0 1 0 140 120 A56 56 0 1 1 70 10Z"/></g>'
            f'<g transform="translate({dx-200},{dy-40}) rotate(-3)"><path {pen} d="M100 150 C40 110 6 80 10 46 C14 14 56 4 100 40 C144 4 186 14 190 46 C194 80 160 110 100 150Z"/></g>')
    # S6 source
    # S7 question
    i = 6
    cells += f'<p class="num" style="left:{i*W+W-f["R"]-300}px;top:236px;font-size:340px;width:320px;text-align:right">6</p>'
    cells += at(i, fmt, L, rule(2) + 40, f'<h2 class="h" style="font-size:100px;width:{W-L-f["R"]}px;text-align:left">What you want to ask.</h2>')
    cells += f'<p class="num" style="left:{i*W+L-16}px;top:{rule(4)-30}px;font-size:460px;color:#F7B6CD;font-style:normal;font-weight:800">&ldquo;</p>'
    cells += at(i, fmt, L, rule(6) - 66, f'<p class="h" style="font-size:100px;font-style:italic;font-weight:600;width:{W-L-f["R"]}px;color:{ROSE};line-height:96px">I think this could be perimenopause. What are my options?</p>')
    cells += f'<p class="num" style="left:{i*W+W-f["R"]-150}px;top:{rule(10)-40}px;font-size:460px;color:#F7B6CD;font-style:normal;font-weight:800">&rdquo;</p>'
    # S8 lockup + app
    i = 7
    cells += lockup(i, fmt, L - 30, 250, 520, dark=True)
    cells += at(i, fmt, L, rule(3) + 30, f'<h2 class="h" style="font-size:80px;width:560px;line-height:96px;font-weight:700">Or let Clari keep the notes, and make a <em>one-page summary</em> for your GP.</h2>')
    cells += at(i, fmt, L, rule(10) - 40, f'<p class="pen" style="font-size:80px;color:{ROSE};width:520px">Save this for the day you book.</p>')
    cells += at(i, fmt, 640, 520, phone('summary.png', 340, rot=6))
    # chrome
    for k in range(N - 1):
        cells += chrome(k, N, fmt, mark='mark-plum.png', ct=106,
                        src=('NHS: symptoms can affect relationships, social life, family life and work.' if k == 5 else None),
                        src_style='max-width:760px;font-size:44px')
    return page(TITLE, fmt, N, cells, svg=svg, css=CSS, light=True, bg='#FBF6EE')


if __name__ == '__main__':
    j, outs = build('c2', 'c2', N, 1440, build_fmt(1440))
    render('c2', [j]); sheet(outs, f'{S}/c2/sheet_1440.jpg')
