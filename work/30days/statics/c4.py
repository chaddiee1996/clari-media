from common import *
import svgkit as K, math

N = 8
TITLE = 'Brain fog translated'
INK = '#241A33'; ROSE = '#B83A68'; LINE = '#4A2070'
PAGES = ['#FCEAF2', '#EFE7FB', '#FFEEDF', '#FFF5D8', '#EAF0FB', '#FBF6EE']
TABS = ['#F7B6CD', '#C3A8EA', '#FFC9A0', '#F3DD8E', '#AFC3F0', '#E8628F']

CSS = """
.page{position:absolute;border-radius:26px;box-shadow:0 30px 60px rgba(34,16,63,.25), 6px 6px 0 #EDE2D3, 12px 12px 0 #E3D6C4;}
.run{font-family:'Figtree',sans-serif;font-weight:800;font-size:40px;letter-spacing:.18em;text-transform:uppercase;color:#B83A68;margin:0}
.hw{font-family:'Fraunces',serif;font-weight:800;font-variation-settings:"opsz" 144;color:#241A33;letter-spacing:-.02em;line-height:.98;margin:0}
.tr{font-family:'Fraunces',serif;font-style:italic;font-weight:600;font-variation-settings:"opsz" 144;color:#B83A68;line-height:1.02;margin:0}
.tab{position:absolute;width:96px;height:150px;border-radius:0 22px 22px 0;display:flex;align-items:center;justify-content:center;font-family:'Fraunces',serif;font-weight:800;font-size:64px;color:#241A33}
.foil{background:linear-gradient(170deg,#FFF3C4 0%,#F5CF84 40%,#FFF0C2 55%,#D9A85A 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
"""

ILL = {
    'colander': '<path d="M-150 -40 L150 -40 Q140 110 0 120 Q-140 110 -150 -40Z"/><path d="M-150 -40 L-200 -60 M150 -40 L200 -60"/><path d="M-60 120 L-80 150 L80 150 L60 120"/>'
                + ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="#4A2070" stroke="none"/>' for x, y in [(-90, 10), (-45, 20), (0, 24), (45, 20), (90, 10), (-60, 60), (-15, 68), (30, 66), (72, 54), (-25, 100), (20, 100)]),
    'remote': '<rect x="-60" y="-170" width="120" height="340" rx="40"/><circle cx="0" cy="-110" r="22"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="12" fill="#4A2070" stroke="none"/>' for x in (-28, 0, 28) for y in (-40, 0, 40, 80)) + '<path d="M-24 130 L24 130"/>',
    'fridge': '<rect x="-110" y="-200" width="220" height="400" rx="26"/><path d="M-110 -60 L110 -60"/><path d="M-80 -160 L-80 -100 M-80 -20 L-80 60"/><path d="M-90 200 L-90 220 M90 200 L90 220"/><path d="M40 -150 l20 0 M40 -130 l40 0" />',
    'badge': '<rect x="-190" y="-120" width="380" height="240" rx="28"/><path d="M-190 -40 L190 -40"/><path d="M-120 60 L120 60" stroke-dasharray="4 18"/><path d="M0 -120 L0 -170 M-30 -170 L30 -170"/>',
    'door': '<path d="M-120 200 L-120 -200 L120 -200 L120 200"/><path d="M-120 -200 L40 -160 L40 230 L-120 200Z" fill="#FFF8EC"/><circle cx="12" cy="20" r="10" fill="#4A2070" stroke="none"/><path d="M-200 200 L200 200"/>',
}

ENTRIES = [
    (1, 'Colander', 'the spaghetti bowl with holes', 'colander'),
    (2, 'Remote control', 'the telly button thing', 'remote'),
    (3, 'Fridge', 'the cold cupboard', 'fridge'),
    (4, 'Her name <span style="font-weight:600;font-size:.5em;letter-spacing:0;display:block;margin-top:14px;color:#5F556B">(20 years of friendship)</span>', 'Hello, <span style="font-style:italic">you</span>!', 'badge'),
    (5, 'Why I came in here', '...', 'door'),
]


def cloud(x, y, s, op=.75):
    return (f'<g transform="translate({x},{y}) scale({s})" opacity="{op}" fill="#FFFFFF">'
            '<ellipse cx="0" cy="0" rx="150" ry="52"/><circle cx="-60" cy="-30" r="58"/><circle cx="30" cy="-52" r="74"/><circle cx="100" cy="-14" r="48"/></g>')


def build_fmt(fmt):
    f = FMT[fmt]; W, H = f['W'], f['H']; PW = W * N
    svg = K.DEFS
    for (x, y, s) in [(820, 1180, 1.4), (1180, 260, 1.0), (2100, 1250, 1.6), (3260, 330, 1.2), (4300, 1230, 1.3), (5380, 300, 1.0), (6470, 1260, 1.5), (7400, 420, 1.2), (7900, 1200, 1.0)]:
        svg += cloud(x, y, s)
    cells = ''
    px, py, pw, ph = 70, 190, 872, 1110
    # slide 1: the cover
    cells += (f'<div class="abs" style="left:{px+40}px;top:{py}px;width:{pw-80}px;height:{ph-10}px;border-radius:18px 30px 30px 18px;'
              f'background:linear-gradient(135deg,#5A2A8C,#3A1766 60%,#2A1150);box-shadow:0 40px 80px rgba(34,16,63,.45), inset 34px 0 0 rgba(0,0,0,.18), inset 40px 0 0 rgba(255,255,255,.06);transform:rotate(-2deg);'
              f'display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 90px 80px 120px;box-sizing:border-box">'
              f'<div style="position:absolute;inset:40px 40px 40px 74px;border:3px solid rgba(245,207,132,.55);border-radius:12px"></div>'
              f'<img src="../assets/mark.png" style="width:150px;margin-bottom:50px;filter:drop-shadow(0 6px 12px rgba(0,0,0,.3))">'
              f'<h1 class="h foil" style="font-size:132px;text-align:center;line-height:1.0">Brain fog,</h1>'
              f'<h1 class="h" style="font-size:132px;text-align:center;line-height:1.05"><em>translated.</em></h1>'
              f'<div style="width:220px;height:3px;background:rgba(245,207,132,.6);margin-top:60px"></div></div>')
    # entry pages
    for k, (i, hw, tr, ill) in enumerate(ENTRIES):
        rot = [-1.2, 0.9, -0.7, 1.1, -0.9][k]
        tabY = py + 120 + k * 170
        cells += (f'<div class="abs" style="left:{i*W+px}px;top:{py}px;width:{pw}px;height:{ph}px;transform:rotate({rot}deg)">'
                  f'<div class="page" style="left:0;top:0;width:{pw}px;height:{ph}px;background:{PAGES[k]};padding:70px 80px;box-sizing:border-box;display:flex;flex-direction:column">'
                  f'<div style="display:flex;justify-content:space-between;align-items:center;border-bottom:3px solid rgba(184,58,104,.35);padding-bottom:22px"><p class="run">Brain fog, translated</p></div>'
                  f'<div style="height:70px"></div>'
                  f'<p class="hw" style="font-size:{132 if len(hw) < 16 else 116}px">{hw}</p>'
                  f'<div style="display:flex;align-items:center;gap:24px;margin-top:40px"><svg width="90" height="40" viewBox="0 0 90 40"><path d="M4 20H80M62 4l18 16-18 16" fill="none" stroke="#B83A68" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                  f'<span class="lab" style="font-size:40px;color:#5F556B;letter-spacing:.16em">translated</span></div>'
                  f'<p class="tr" style="font-size:{"104px" if len(tr) > 8 else "300px;line-height:.6"};margin-top:22px">{tr if tr != "..." else "&hellip;"}</p>'
                  f'<div style="flex:1"></div></div>'
                  f'<div class="tab" style="left:{pw-4}px;top:{tabY-py}px;background:{TABS[k]};box-shadow:6px 6px 14px rgba(34,16,63,.18)">{hw[0]}</div></div>')
        # illustration, bottom right of the page, line-art
        ix, iy = i * W + px + pw - 230, py + ph - 250
        svg_ill = f'<g transform="translate({ix},{iy}) rotate({rot}) scale(.9)" fill="none" stroke="{LINE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity=".9">{ILL[ill]}</g>'
        cells += f'<svg class="abs" style="left:0;top:0;pointer-events:none" width="{PW}" height="{H}">{svg_ill}</svg>' if False else ''
        svg_top = svg_ill
        cells += f'<svg class="abs" style="left:{ix-260}px;top:{iy-260}px" width="520" height="520" viewBox="{ix-260} {iy-260} 520 520">{svg_top}</svg>'
    # slide 7: the fact, as a usage note
    i = 6
    cells += (f'<div class="abs" style="left:{i*W+px}px;top:{py}px;width:{pw}px;height:{ph}px;transform:rotate(0.6deg)">'
              f'<div class="page" style="left:0;top:0;width:{pw}px;height:{ph}px;background:#FBF6EE;padding:70px 80px;box-sizing:border-box;display:flex;flex-direction:column">'
              f'<div style="border-bottom:3px solid rgba(184,58,104,.35);padding-bottom:22px"><p class="run">Brain fog, translated</p></div>'
              f'<div style="flex:1"></div>'
              f'<div style="border-left:12px solid #F7B6CD;padding-left:46px">'
              f'<p class="h" style="font-size:96px;color:#241A33;line-height:1.06">Problems with memory and concentration are on the NHS list of perimenopause <em style="color:#B83A68">symptoms.</em></p></div>'
              f'<div style="flex:1"></div><p class="s" style="font-size:44px;color:#241A33">Source: NHS</p></div></div>')
    # slide 8: the back cover with the lockup
    i = 7
    cells += (f'<div class="abs" style="left:{i*W+px+40}px;top:{py}px;width:{pw-80}px;height:{ph-10}px;border-radius:30px 18px 18px 30px;'
              f'background:linear-gradient(135deg,#5A2A8C,#3A1766 60%,#2A1150);box-shadow:0 40px 80px rgba(34,16,63,.45), inset -34px 0 0 rgba(0,0,0,.18);transform:rotate(1.6deg);'
              f'display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 110px;box-sizing:border-box">'
              f'<div style="position:absolute;inset:40px 74px 40px 40px;border:3px solid rgba(245,207,132,.55);border-radius:12px"></div>'
              f'<img src="../assets/lockup-light.png" style="width:560px;margin-bottom:70px">'
              f'<h2 class="h" style="font-size:92px;text-align:center;line-height:1.06">Send this to the one who knows exactly what you <em>mean.</em></h2></div>')
    for k in range(N - 1):
        cells += chrome(k, N, fmt, ct=70)
    js = """function draw(){ CLARI.sky(c,'day',PW,H,{glow:0});
      for(let i=0;i<N;i++){ const g=c.createRadialGradient(i*W+W*0.8,H*0.15,10,i*W+W*0.8,H*0.15,W); g.addColorStop(0,'rgba(255,240,245,0.35)'); g.addColorStop(1,'rgba(255,240,245,0)'); c.fillStyle=g; c.fillRect(i*W-W,0,W*3,H);}
      for(let k=0;k<26;k++){ const x=(k*397)%PW, y=200+((k*613)%1100); CLARI.petal(c,x,y,0.9+(k%3)*0.3,k*0.7,0.8); }
    }"""
    return page(TITLE, fmt, N, cells, js=js, svg=svg, css=CSS, bg='#9A90E2')


if __name__ == '__main__':
    j, outs = build('c4', 'c4', N, 1440, build_fmt(1440))
    render('c4', [j]); sheet(outs, f'{S}/c4/sheet_1440.jpg')
