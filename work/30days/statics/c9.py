from common import *
import svgkit as K, math

N = 7
TITLE = 'What Clari keeps'


def build_fmt(fmt):
    f = FMT[fmt]; W, H = f['W'], f['H']; PW = W * N
    svg = K.DEFS
    cells = ''
    L, R = f['L'], f['R']
    # S1: a giant crescent holds the phone
    cells += cell(0, fmt, '<h1 class="h" style="font-size:118px">Your symptoms are nobody\'s business but <em>yours.</em></h1>', pad=(190, 0, L, R))
    cells += at(0, fmt, 430, 690, phone('home.png', 370, rot=-8))
    # S2 stored on your phone: phone left, text right
    cells += at(1, fmt, 70, 330, phone('home.png', 430, rot=-4))
    cells += cell(1, fmt, '<div style="flex:1"></div><h2 class="h" style="font-size:112px;text-align:right">Stored on your <em>phone.</em></h2><div style="flex:1.3"></div>', pad=(190, 190, 560, R))
    # S3 no account: text big top, phone low right cropped by the frame
    cells += cell(2, fmt, '<h2 class="h" style="font-size:132px">No account needed to <em>start.</em></h2>', pad=(200, 0, L, 260))
    cells += at(2, fmt, 470, 690, phone('done.png', 420, rot=7))
    # S4 you choose: a close crop of the real Share Summary card
    cells += cell(3, fmt, '<h2 class="h" style="font-size:112px;text-align:center">You choose what to share, and <em>when.</em></h2>', pad=(200, 0, L, R))
    crop_w = 860
    sc = crop_w / 1210
    crop_h = 950 * sc
    cells += (f'<div class="abs" style="left:{3*W+(W-crop_w)/2}px;top:600px;width:{crop_w}px;height:{crop_h:.0f}px;border-radius:56px;overflow:hidden;'
              f'box-shadow:0 40px 80px rgba(16,4,40,.5), 0 0 0 10px #16101F;transform:rotate(-2deg)">'
              f'<img src="../assets/summary.png" style="position:absolute;left:{-40*sc:.0f}px;top:{-1160*sc:.0f}px;width:{1290*sc:.0f}px"></div>')
    # S5 summary: phone right, text left
    cells += at(4, fmt, 560, 300, phone('summary.png', 420, rot=4))
    cells += cell(4, fmt, '<div style="flex:1"></div><h2 class="h" style="font-size:88px">A one-page summary for your GP, from your own <em>notes.</em></h2><div style="flex:1"></div>', pad=(190, 190, L, 560))
    # S6 track: two phones, triggers behind log
    cells += at(5, fmt, 520, 640, phone('triggers.png', 340, rot=10, extra='opacity:.95'))
    cells += at(5, fmt, 170, 600, phone('log.png', 380, rot=-5))
    cells += cell(5, fmt, '<h2 class="h" style="font-size:94px;text-align:right">Track symptoms, triggers and your cycle in under a <em>minute</em> a day.</h2>', pad=(190, 0, L, R))
    # S7 lockup
    cells += lockup(6, fmt, W / 2, 380, 680, center=True)
    cells += cell(6, fmt, '<div style="height:520px"></div><h2 class="h" style="font-size:100px;text-align:center">Free on the App Store and <em style="white-space:nowrap">Google Play.</em></h2>', pad=(190, 0, L, R))
    # continuity: a trail of petals and a dotted orbit through all slides
    pts = [(0.85 * W, 520), (1.5 * W, 300), (2.35 * W, 560), (3.5 * W, 560), (4.3 * W, 1220), (5.6 * W, 520), (6.3 * W, 300)]
    d = f'M{pts[0][0]:.0f},{pts[0][1]:.0f}' + ''.join(f' Q{(a[0]+b[0])/2:.0f},{(a[1]+b[1])/2 - 200:.0f} {b[0]:.0f},{b[1]:.0f}' for a, b in zip(pts, pts[1:]))
    svg += f'<path d="{d}" fill="none" stroke="#E9DAFF" stroke-opacity=".35" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/>'
    hb = H - 200
    svg += K.hills(PW, H, hb - 40, 50, seed=3.1, fill='#4A2180', op=.85, waves=(0.0011, 0.0027, 0.0063)) + K.hills(PW, H, hb + 40, 30, seed=0.4, fill='#1C0B36', waves=(0.0012, 0.0031, 0.0071))
    for k in range(N - 1):
        cells += chrome(k, N, fmt)
    js = """function draw(){ CLARI.sky(c,'night',PW,H,{glow:0});
      for(let i=0;i<N;i++){ const g=c.createRadialGradient(i*W+W*0.5,H*0.45,10,i*W+W*0.5,H*0.45,W*0.9); g.addColorStop(0,'rgba(195,168,234,0.14)'); g.addColorStop(1,'rgba(195,168,234,0)'); c.fillStyle=g; c.fillRect(i*W-W,0,W*3,H);}
      CLARI.stars(c,PW,H,0.2,{seed:41,n:1100,bottom:0.85,alpha:0.8,sparkles:24});
      CLARI.moon(c, W*0.52, 1040, 360, {glow:1});
      CLARI.branch(c2, 7*W+40, H-470, 2.4, true, 0, {blossoms:7});
      for(let k=0;k<16;k++){ const x=W*0.9+k*(PW-W*1.6)/16, y=300+((k*517)%800); CLARI.petal(c2,x,y,0.9+(k%3)*0.25,k*0.9,0.75); }
    }"""
    return page(TITLE, fmt, N, cells, js=js, svg=svg)


if __name__ == '__main__':
    j, outs = build('c9', 'c9', N, 1440, build_fmt(1440))
    render('c9', [j]); sheet(outs, f'{S}/c9/sheet_1440.jpg')
