from common import *
import svgkit as K, math

N = 7
TITLE = 'Menopause at work'
SRC = 'Source: GOV.UK, Office for Equality and Opportunity, 2026'
INK = '#22103F'
CSS = """
.h{color:#22103F} .h em{color:#B83A68}
.mon{font-family:'Figtree',sans-serif;font-weight:800;font-size:40px;letter-spacing:.08em;color:#4A2070;margin:0;text-align:center}
.yr{font-family:'Fraunces',serif;font-weight:700;font-size:56px;color:#22103F;margin:0}
"""
MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


def build_fmt(fmt):
    f = FMT[fmt]; W, H = f['W'], f['H']; PW = W * N
    top, sill = 176, 930           # window glass from top to sill
    svg = K.DEFS
    cells = ''
    # wall
    svg += f'<rect x="0" y="0" width="{PW}" height="{H}" fill="#EFE6F4"/>'
    # glass: sky is drawn on canvas, the svg wall frame is cut out with a mask
    svg += f'<mask id="glass"><rect width="{PW}" height="{H}" fill="#fff"/><rect x="0" y="{top}" width="{PW}" height="{sill-top}" fill="#000"/></mask>'
    svg = svg.replace('<rect x="0" y="0" width="{PW}" height="{H}" fill="#EFE6F4"/>'.format(PW=PW, H=H), f'<rect x="0" y="0" width="{PW}" height="{H}" fill="#EFE6F4" mask="url(#glass)"/>')
    # clouds behind the glass
    svg += f'<clipPath id="gc"><rect x="0" y="{top}" width="{PW}" height="{sill-top}"/></clipPath><g clip-path="url(#gc)">'
    for (x, y, s) in [(760, 330, 1.1), (1900, 330, 0.8), (2500, 300, .9), (4600, 360, 1.3), (5500, 800, 1.0), (6600, 320, 1.1)]:
        svg += (f'<g transform="translate({x},{y}) scale({s})" opacity=".8" fill="#fff"><ellipse cx="0" cy="0" rx="150" ry="50"/><circle cx="-60" cy="-28" r="56"/><circle cx="30" cy="-50" r="72"/><circle cx="100" cy="-12" r="46"/></g>')
    svg += '</g>'
    # frame: mullions exactly on slide edges, so the carousel reads as one long office window
    svg += f'<rect x="0" y="{top-26}" width="{PW}" height="26" fill="#FFFFFF"/><rect x="0" y="{top-6}" width="{PW}" height="6" fill="#D9CCE6"/>'
    for i in range(N + 1):
        svg += f'<rect x="{i*W-20}" y="{top-26}" width="40" height="{sill-top+26}" fill="#FFFFFF"/><rect x="{i*W+14}" y="{top}" width="6" height="{sill-top}" fill="#D9CCE6"/>'
    # sill
    svg += f'<rect x="0" y="{sill}" width="{PW}" height="44" fill="#FFFFFF"/><rect x="0" y="{sill+44}" width="{PW}" height="14" fill="#D9CCE6"/>'
    # glass sheen
    for i in range(N):
        svg += f'<path d="M{i*W+640},{top} L{i*W+780},{top} L{i*W+420},{sill} L{i*W+280},{sill} Z" fill="#fff" opacity=".10"/>'
    # year planner strip pinned under the window, continuous across every slide
    sy = sill + 110
    mw = 216
    x_nov26 = 2 * W + 540
    xs0 = x_nov26 - 10 * mw - mw / 2; xs1 = x_nov26 + 13 * mw + mw / 2
    strip = f'<rect x="{xs0-150}" y="{sy}" width="{xs1-xs0+150}" height="150" rx="10" fill="#FFFFFF" filter="url(#softS)"/>'
    strip += f'<rect x="{xs0-150}" y="{sy}" width="150" height="150" rx="10" fill="#4A2070"/>'
    labels = ''
    for k in range(-10, 14):
        m = (10 + k) % 12  # month index, k=0 is Nov 2026
        yr = 2026 + (10 + k) // 12
        x = x_nov26 + k * mw - mw / 2
        spring = yr == 2027 and m in (2, 3, 4)
        now = (k == 0)
        if spring:
            strip += f'<rect x="{x}" y="{sy}" width="{mw}" height="150" fill="#F7B6CD"/>'
        if now:
            strip += f'<rect x="{x}" y="{sy}" width="{mw}" height="150" fill="#C3A8EA"/>'
        strip += f'<line x1="{x}" x2="{x}" y1="{sy}" y2="{sy+150}" stroke="#E2D6EC" stroke-width="3"/>'
        if 0 <= x < PW:
            i = int(x // W)
            labels += f'<p class="mon abs" style="left:{x}px;top:{sy+24}px;width:{mw}px">{MONTHS[m]}</p>'
            labels += f'<p class="abs" style="left:{x}px;top:{sy+80}px;width:{mw}px;text-align:center;margin:0;font-family:Figtree;font-weight:700;font-size:40px;color:#7A6A8E">{yr}</p>'
    labels += f'<p class="abs" style="left:{xs0-150}px;top:{sy+16}px;width:150px;text-align:center;margin:0;font-family:Fraunces;font-weight:700;font-size:40px;line-height:1.0;color:#FFF8EC">2026<br><span style="font-style:italic;font-weight:600;color:#F7B6CD">to</span><br>2027</p>'
    # bracket labels
    labels += f'<p class="lab abs" style="left:{x_nov26-mw/2-40}px;top:{sy-84}px;width:{mw+80}px;text-align:center;font-size:40px;color:#4A2070">Now</p>'
    sx = x_nov26 + 4 * mw - mw / 2
    labels += f'<p class="lab abs" style="left:{sx}px;top:{sy-70}px;width:{3*mw}px;text-align:center;font-size:40px;color:#B83A68">Spring 2027</p>'
    strip += f'<path d="M{x_nov26},{sy-14} L{x_nov26-14},{sy-30} L{x_nov26+14},{sy-30} Z" fill="#4A2070"/>'
    strip += f'<path d="M{sx+8},{sy-14} L{sx+8},{sy-24} L{sx+3*mw-8},{sy-24} L{sx+3*mw-8},{sy-14}" fill="none" stroke="#B83A68" stroke-width="5" stroke-linecap="round"/>'
    svg += strip
    cells += labels
    # pins
    for x in range(int(xs0) + 300, int(xs1), 760):
        svg += f'<circle cx="{x}" cy="{sy+14}" r="12" fill="#E8628F"/>'
    # objects on the sill
    plant = ('<path d="M-60 0 L60 0 L48 -110 L-48 -110 Z" fill="#E8628F"/><rect x="-56" y="-122" width="112" height="22" rx="6" fill="#B83A68"/>'
             '<path d="M0 -120 C-80 -170 -110 -250 -60 -300 C-20 -240 -10 -180 0 -120Z" fill="#8FB59B"/><path d="M0 -120 C60 -200 120 -220 140 -280 C70 -270 20 -220 0 -120Z" fill="#7AA387"/><path d="M0 -120 C-10 -200 10 -280 30 -330 C50 -260 30 -180 0 -120Z" fill="#9DC2A8"/>')
    mug = ('<path d="M60 -100 C110 -100 110 -30 60 -30" fill="none" stroke="#7A45B5" stroke-width="18"/><path d="M-70 -140 L70 -140 L62 -10 Q60 0 48 0 L-48 0 Q-60 0 -62 -10Z" fill="#C3A8EA"/>'
           '<path d="M-20 -170 C-40 -200 0 -210 -20 -240 M20 -170 C0 -200 40 -210 20 -250" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round"/>')
    svg += f'<g transform="translate({W*0.78},{sill+4}) scale(1.05)" filter="url(#softS)">{plant}</g><g transform="translate({W*0.58},{sill+4})" filter="url(#softS)">{mug}</g>'
    # S5 clipboard leaning on the sill
    cb = ('<rect x="-170" y="-470" width="340" height="470" rx="22" fill="#B9A0DA"/><rect x="-140" y="-430" width="280" height="410" rx="10" fill="#FFFFFF"/>'
          '<rect x="-60" y="-490" width="120" height="50" rx="14" fill="#7A45B5"/>'
          + ''.join(f'<rect x="-110" y="{-370+k*80}" width="34" height="34" rx="8" fill="none" stroke="#7A45B5" stroke-width="5"/><path d="M-104 {-354+k*80} l10 12 l22 -28" fill="none" stroke="#E8628F" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
                    f'<rect x="-56" y="{-362+k*80}" width="{150 - (k%2)*40}" height="16" rx="8" fill="#DCCFEA"/>' for k in range(4)))
    svg += f'<g transform="translate({4*W+W*0.74},{sill+6}) rotate(-6)" filter="url(#soft)">{cb}</g>'
    # S2: 250 dots
    dots = ''
    for k in range(250):
        r_, c_ = divmod(k, 25)
        dots += f'<circle cx="{1*W+f["L"]+14+c_*30}" cy="{sill-56-(9-r_)*30}" r="9.5" fill="#4A2070" opacity=".85"/>'
    svg += dots
    # S6: a sticky note on the glass
    cells += (f'<div class="abs" style="left:{5*W+190}px;top:{470}px;width:700px;height:400px;background:linear-gradient(170deg,#FCD3E1,#F7B6CD);transform:rotate(-3deg);'
              f'box-shadow:0 18px 30px rgba(34,16,63,.22);padding:50px 56px;box-sizing:border-box">'
              f'<div style="position:absolute;left:280px;top:-24px;width:140px;height:46px;background:rgba(255,255,255,.55);transform:rotate(2deg)"></div>'
              f'<p class="hand" style="font-size:94px;color:#22103F;margin:0;line-height:1.0">do we have a menopause action plan?</p></div>')
    # text in the panes
    T = top + 70
    cells += cell(0, fmt, f'''<h1 class="h" style="font-size:132px">Menopause<br>at work.</h1>
        <h2 class="h" style="font-size:88px;margin-top:40px">Here's what's <em>changing.</em></h2>''', pad=(T, 0, f['L'] + 10, f['R']))
    cells += cell(1, fmt, '<h2 class="h" style="font-size:84px;max-width:880px">Employers with 250 or more staff can now publish a menopause <em>action plan.</em></h2>', pad=(T, 0, f['L'] + 10, f['R']))
    cells += cell(2, fmt, '<div style="flex:.8"></div><h2 class="h" style="font-size:136px;text-align:center">Right now it\'s <em>voluntary.</em></h2><div style="flex:1.8"></div>', pad=(top, H - sill, f['L'], f['R']))
    cells += cell(3, fmt, '<h2 class="h" style="font-size:96px;text-align:right">Subject to legislation, it becomes mandatory from <em>spring 2027.</em></h2>', pad=(T, 0, f['L'], f['R'] + 10))
    cells += cell(4, fmt, '<h2 class="h" style="font-size:80px;max-width:560px">The plans show the steps employers are taking to support employees experiencing <em>menopause.</em></h2>', pad=(T, 0, f['L'] + 10, f['R']))
    cells += cell(5, fmt, '<h2 class="h" style="font-size:104px;text-align:center">Worth asking <em>at work:</em></h2>', pad=(T, 0, f['L'], f['R']))
    cells += lockup(6, fmt, W / 2, T - 10, 600, dark=True, center=True)
    cells += cell(6, fmt, '<div style="height:330px"></div><h2 class="h" style="font-size:118px;text-align:center">Send this to a <em>colleague.</em></h2>', pad=(T, 0, f['L'], f['R']))
    for k in range(N - 1):
        cells += chrome(k, N, fmt, src=SRC, mark='mark-plum.png', ct=46, src_style='max-width:880px;font-size:44px')
    # top wall is short: put the mark/counter in the wall strip above the glass
    js = """function draw(){
      const g=c.createLinearGradient(0,176,0,930); const s=CLARI.SKIES.day; [0,.36,.66,.86,1].forEach((p,k)=>g.addColorStop(p,s[k])); c.fillStyle=g; c.fillRect(0,0,PW,H);
      for(let i=0;i<N;i++){ const r=c.createRadialGradient(i*W+W*0.75,300,10,i*W+W*0.75,300,W*0.8); r.addColorStop(0,'rgba(255,240,245,0.35)'); r.addColorStop(1,'rgba(255,240,245,0)'); c.fillStyle=r; c.fillRect(i*W-W,0,W*3,H); }
      CLARI.moon(c, 6*W+W*0.82, 300, 46, {glow:0.4});
      CLARI.branch(c2, 3*W+40, 650, 2.6, true, 0, {blossoms:7});
      CLARI.branch(c2, 3*W-40, 660, 2.4, false, 0, {blossoms:6});
    }"""
    return page(TITLE, fmt, N, cells, js=js, svg=svg, css=CSS, light=True, bg='#EFE6F4')


if __name__ == '__main__':
    j, outs = build('c6', 'c6', N, 1440, build_fmt(1440))
    render('c6', [j]); sheet(outs, f'{S}/c6/sheet_1440.jpg')
