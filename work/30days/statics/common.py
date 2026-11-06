"""Shared scaffolding for Clari 30-day statics.
A carousel is ONE wide panorama page (N x 1080 wide). Each slide is a 1080 viewport into it, so art that
crosses a slide edge really continues on the next slide. Text lives in per-slide 'cells' (DOM, crisp)."""
import os, json, subprocess, html as _h
from PIL import Image

S = '/home/claude/clari-media/work/30days/statics'
OUT = '/home/claude/clari/30 days'

# format: safe areas. T/B = content padding top/bottom, L/R side padding. ct = chrome top. sb = source bottom.
FMT = {
    1440: dict(W=1080, H=1440, T=190, B=190, L=88, R=88, ct=70, sb=72),
    1920: dict(W=1080, H=1920, T=340, B=560, L=88, R=170, ct=230, sb=432),
}

P = dict(night='#22103F', plum='#4A2070', violet='#7A45B5', lilac='#C3A8EA', cream='#FFF8EC', pink='#F7B6CD',
         blossom='#E8628F', rose='#B83A68', gold='#FFEFC9', paper='#FBF6EE', ink='#241A33', deep='#2A1548')

BASE_CSS = """
:root{--night:#22103F;--plum:#4A2070;--violet:#7A45B5;--lilac:#C3A8EA;--cream:#FFF8EC;--pink:#F7B6CD;
--blossom:#E8628F;--rose:#B83A68;--gold:#FFEFC9;--paper:#FBF6EE;--ink:#241A33;--deep:#2A1548}
html,body{margin:0;padding:0;overflow:hidden;background:#22103F}
#stage{position:absolute;left:0;top:0;transform-origin:0 0}
#art,#svg{position:absolute;left:0;top:0}
.cell{position:absolute;top:0;box-sizing:border-box;display:flex;flex-direction:column}
.cell>*{flex-shrink:0}
.abs{position:absolute}
.h{font-family:'Fraunces',serif;font-weight:700;font-variation-settings:"opsz" 144;letter-spacing:-0.012em;word-spacing:0.05em;line-height:1.04;margin:0;color:var(--cream)}
.h em{font-style:italic;font-weight:600;color:var(--pink);letter-spacing:-0.01em}
.light .h{color:var(--ink)} .light .h em{color:var(--rose)}
.s{font-family:'Figtree',sans-serif;font-weight:700;color:var(--cream);margin:0;line-height:1.25}
.light .s{color:var(--ink)}
.lab{font-family:'Figtree',sans-serif;font-weight:800;letter-spacing:.16em;text-transform:uppercase;margin:0}
.hand{font-family:'Caveat',cursive;font-weight:700;line-height:1.05}
.chrome-mark{position:absolute;height:86px}
.counter{position:absolute;font-family:'Figtree',sans-serif;font-weight:700;font-size:42px;letter-spacing:.04em;color:var(--cream);opacity:.9;line-height:86px;font-variant-numeric:tabular-nums}
.src{position:absolute;font-family:'Figtree',sans-serif;font-weight:700;font-size:44px;color:var(--cream);opacity:.92;line-height:1.15;margin:0}
.light .counter,.light .src{color:var(--ink)}
.lock{position:absolute}
"""


def esc(t):
    return _h.escape(t, quote=False)


def page(title, fmt, n, cells, js='', svg='', css='', light=False, bg='#22103F', imgs=()):
    f = FMT[fmt]
    W, H = f['W'], f['H']
    imgs_js = json.dumps(list(imgs))
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{esc(title)}</title>
<link rel="stylesheet" href="../fonts/fonts.css">
<style>{BASE_CSS}
html,body{{width:{W}px;height:{H}px;background:{bg}}}
{css}</style></head>
<body class="{'light' if light else 'dark'}"><div id="stage" style="width:{W*n}px;height:{H}px">
<canvas id="art" width="{W*n}" height="{H}"></canvas>
<svg id="svg" width="{W*n}" height="{H}" viewBox="0 0 {W*n} {H}" xmlns="http://www.w3.org/2000/svg">{svg}</svg>
<canvas id="art2" width="{W*n}" height="{H}" style="position:absolute;left:0;top:0"></canvas>
{cells}
</div>
<script src="../assets/clari-art.js"></script>
<script>
const W={W}, H={H}, N={n}, PW={W*n};
const c=document.getElementById('art').getContext('2d'); const c2=document.getElementById('art2').getContext('2d');
const IM={{}};
function loadAll(list){{return Promise.all(list.map(n=>new Promise(r=>{{const i=new Image();i.onload=()=>r();i.onerror=()=>r();i.src='../assets/'+n;IM[n]=i;}})));}}
function show(i){{document.getElementById('stage').style.transform='translateX('+(-i*W)+'px)';}}
{js}
Promise.all([document.fonts.ready, loadAll({imgs_js})]).then(()=>{{ if(typeof draw==='function') draw(); show(0); window.__ready=true; }});
</script></body></html>"""


def cell(i, fmt, inner, style='', cls='', pad=None):
    """A per-slide flex column box inside the safe area."""
    f = FMT[fmt]
    T, B, L, R = pad if pad else (f['T'], f['B'], f['L'], f['R'])
    return (f'<div class="cell {cls}" style="left:{i*f["W"]}px;width:{f["W"]}px;height:{f["H"]}px;'
            f'padding:{T}px {R}px {B}px {L}px;{style}">{inner}</div>')


def at(i, fmt, x, y, inner, style='', cls=''):
    f = FMT[fmt]
    return f'<div class="abs {cls}" style="left:{i*f["W"]+x}px;top:{y}px;{style}">{inner}</div>'


def chrome(i, n, fmt, src=None, mark='mark.png', counter=True, src_style='', ct=None):
    """small mark top-left, counter top-right, source bottom-left. Same corner on every slide."""
    f = FMT[fmt]
    x0 = i * f['W']
    ct = f['ct'] if ct is None else ct
    o = f'<img class="chrome-mark" src="../assets/{mark}" style="left:{x0+f["L"]}px;top:{ct}px">'
    if counter:
        o += (f'<div class="counter" style="left:{x0}px;width:{f["W"]-f["R"]}px;text-align:right;top:{ct}px">'
              f'{i+1}/{n}</div>')
    if src:
        o += (f'<p class="src" style="left:{x0+f["L"]}px;bottom:{f["sb"]}px;max-width:{f["W"]-f["L"]-f["R"]}px;{src_style}">'
              f'{src}</p>')
    return o


def lockup(i, fmt, x, y, w, dark=False, center=False):
    f = FMT[fmt]
    src = 'lockup-dark.png' if dark else 'lockup-light.png'
    left = i * f['W'] + (x - w / 2 if center else x)
    return f'<img class="lock" src="../assets/{src}" style="left:{left}px;top:{y}px;width:{w}px">'


def render(folder, jobs):
    jp = os.path.join(S, folder, 'jobs.json')
    json.dump(jobs, open(jp, 'w'))
    r = subprocess.run(['nice', '-n', '5', 'node', os.path.join(S, 'render.js'), jp], capture_output=True, text=True)
    if r.returncode or 'ERROR' in r.stderr or 'not ready' in r.stderr:
        print(r.stderr)


def sheet(pngs, out, cols=3, w=360):
    ims = [Image.open(p).convert('RGB') for p in pngs]
    h = round(ims[0].height * w / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    s = Image.new('RGB', (cols * w + (cols - 1) * 8, rows * h + (rows - 1) * 8), '#888')
    for k, im in enumerate(ims):
        s.paste(im.resize((w, h), Image.LANCZOS), ((k % cols) * (w + 8), (k // cols) * (h + 8)))
    s.save(out, quality=90)


def export(pngs, dest):
    os.makedirs(dest, exist_ok=True)
    for k, p in enumerate(pngs):
        Image.open(p).convert('RGB').save(os.path.join(dest, f'{k+1:02d}.jpg'), quality=92, subsampling=0)


def build(folder, name, n, fmt, html):
    d = os.path.join(S, folder)
    os.makedirs(d, exist_ok=True)
    hp = os.path.join(d, f'{name}_{fmt}.html')
    open(hp, 'w').write(html)
    outs = [os.path.join(d, f'{name}_{fmt}_{k+1:02d}.png') for k in range(n)]
    return dict(html=hp, w=1080, h=fmt, slides=[dict(i=k, out=o) for k, o in enumerate(outs)]), outs


def phone(screen, w, rot=0, shadow=True, extra=''):
    """DOM phone frame around a real app screenshot (crisper than canvas)."""
    h = w * 2796 / 1290
    bez = w * 0.035
    R = w * 0.16
    sh = 'box-shadow:0 %dpx %dpx rgba(16,4,40,.45), inset 0 0 0 %.1fpx rgba(255,255,255,.14);' % (w * .08, w * .2, max(1, w * .004)) if shadow else ''
    return (f'<div style="width:{w+2*bez:.0f}px;height:{h+2*bez:.0f}px;border-radius:{R+bez:.0f}px;background:#16101F;{sh}'
            f'transform:rotate({rot}deg);box-sizing:border-box;padding:{bez:.1f}px;{extra}">'
            f'<img src="../assets/{screen}" style="display:block;width:{w:.0f}px;height:{h:.0f}px;border-radius:{R:.0f}px"></div>')
