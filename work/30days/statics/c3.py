from common import *
import svgkit as K, math, json

N = 9
TITLE = 'Self Care Week'
SKY = [
    ['#160A2C', '#33196A', '#6743A3', '#B97DB9', '#F0AFB0'],   # 1 before dawn
    ['#3A2470', '#7A52B4', '#D58DB9', '#F8B7A9', '#FFDDB5'],   # MON dawn
    ['#6A63C9', '#9C86DA', '#E0A9D2', '#FBCDBF', '#FFE6C8'],   # TUE morning
    ['#6B7BD8', '#9A90E2', '#C6A9EA', '#EBC6EA', '#FBE0EC'],   # WED day
    ['#7A82DA', '#A495E2', '#D5ADE6', '#F4C7DB', '#FFDCCB'],   # THU afternoon
    ['#4D3A9A', '#8E5FB8', '#E28BB0', '#FBB496', '#FFD7A0'],   # FRI golden hour
    ['#150929', '#391766', '#7742AE', '#C47CBD', '#F7B9CB'],   # SAT evening
    ['#120723', '#2C1252', '#4A2180', '#6F3FA6', '#8E57BE'],   # SUN night
    ['#0E061D', '#22103F', '#3C1A6E', '#5D3194', '#7A45B5'],   # end
]
HILL = ['#4B2A80', '#7A4FA8', '#8F78C8', '#8E84D6', '#9A86D2', '#7A4699', '#3E1C6C', '#2A1150', '#1E0C3C']
HILL2 = ['#2C1356', '#55347F', '#6E5AB0', '#6F66BE', '#7963B8', '#552A78', '#26104A', '#180934', '#12072A']
DAYS = [
    (1, 'MON', '16', 'Go to bed at the <em>same</em> time as last night.', 'pillow', 'left', False),
    (2, 'TUE', '17', 'Put a <em>cold</em> drink by the bed.', 'glass', 'right', True),
    (3, 'WED', '18', 'Take a walk while it\'s still <em>light.</em>', 'path', 'left', True),
    (4, 'THU', '19', 'Tell one person how you\'re <em>really</em> doing.', 'mugs', 'right', True),
    (5, 'FRI', '20', 'Ten <em>quiet</em> minutes. Yoga, tai chi, or meditation.', 'candle', 'left', False),
    (6, 'SAT', '21', 'Something with <em>calcium.</em> Milk, yoghurt, kale.', 'milk', 'right', False),
    (7, 'SUN', '22', 'Write down how this week really <em>felt.</em>', 'book', 'left', False),
]

INKC = '#22103F'


def grad(id_, stops, vertical=True):
    a = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    return f'<linearGradient id="{id_}" {a}>' + ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + '</linearGradient>'


def objects():
    """flat objects in local coords, origin = bottom centre (sits on the ground)."""
    o = {}
    o['pillow'] = (grad('pl', [(0, '#FFF8EC'), (1, '#E6D6F3')]) + grad('ck', [(0, '#6A3BA0'), (1, '#3E1C6C')]) +
                   '<path filter="url(#soft)" d="M-300 0 C-330 -40 -320 -150 -280 -170 C-150 -200 120 -200 270 -172 C320 -150 330 -40 300 0 C120 14 -120 14 -300 0Z" fill="url(#pl)"/>'
                   '<path d="M-230 -110 C-120 -126 120 -126 230 -108" stroke="#D9C6EC" stroke-width="5" fill="none" stroke-linecap="round"/>'
                   '<g transform="translate(250,-170)"><rect x="-18" y="70" width="12" height="44" rx="6" fill="#3E1C6C"/><rect x="18" y="70" width="12" height="44" rx="6" fill="#3E1C6C"/>'
                   '<circle cx="0" cy="0" r="112" fill="url(#ck)" filter="url(#softS)"/><circle r="88" fill="#FFF8EC"/>'
                   + ''.join(f'<rect x="-3" y="-80" width="6" height="16" rx="3" fill="#C3A8EA" transform="rotate({k*30})"/>' for k in range(12)) +
                   '<rect x="-5" y="-56" width="10" height="60" rx="5" fill="#22103F" transform="rotate(-60)"/><rect x="-4" y="-72" width="8" height="76" rx="4" fill="#B83A68" transform="rotate(0)"/><circle r="10" fill="#22103F"/>'
                   '<circle cx="-70" cy="-96" r="26" fill="#6A3BA0"/><circle cx="70" cy="-96" r="26" fill="#6A3BA0"/></g>')
    o['glass'] = (grad('gl', [(0, 'rgba(255,255,255,.75)'), (1, 'rgba(232,220,250,.55)')]) + grad('wt', [(0, '#CFE2FA'), (1, '#9DB5EE')]) +
                  '<ellipse cx="0" cy="0" rx="210" ry="26" fill="#22103F" opacity=".18"/>'
                  '<path d="M-130 -470 L130 -470 L108 -10 Q106 6 90 6 L-90 6 Q-106 6 -108 -10Z" fill="url(#gl)" filter="url(#soft)"/>'
                  '<path d="M-122 -340 L122 -340 L108 -10 Q106 6 90 6 L-90 6 Q-106 6 -108 -10Z" fill="url(#wt)" opacity=".9"/>'
                  '<rect x="-80" y="-380" width="86" height="86" rx="18" fill="#F4FAFF" opacity=".92" transform="rotate(-12 -37 -337)"/>'
                  '<rect x="10" y="-330" width="80" height="80" rx="18" fill="#EAF3FF" opacity=".9" transform="rotate(14 50 -290)"/>'
                  '<rect x="-60" y="-240" width="70" height="70" rx="16" fill="#E2EEFF" opacity=".7" transform="rotate(8 -25 -205)"/>'
                  '<path d="M-96 -440 L-78 -40" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity=".6"/>'
                  + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="10" fill="#fff" opacity=".7"/>' for x, y in [(70, -420), (96, -380), (60, -150), (88, -110), (-40, -60)]))
    o['path'] = (grad('pa', [(0, '#FBE6EE'), (1, '#F3C9DC')]) +
                 '<path d="M-40 -300 C-10 -240 60 -210 40 -150 C20 -90 -160 -60 -260 0 L120 0 C150 -70 220 -110 210 -170 C200 -230 40 -250 -20 -300Z" fill="url(#pa)" opacity=".95"/>'
                 + ''.join(f'<g transform="translate({x},{y}) scale({s})"><rect x="-7" y="-10" width="14" height="70" rx="6" fill="#3E1C6C"/><circle cx="0" cy="-40" r="56" fill="#5A2C93"/><circle cx="-16" cy="-56" r="26" fill="#7A45B5" opacity=".7"/></g>'
                           for x, y, s in [(-330, -100, 1.3), (-200, -230, .8), (300, -150, 1.1), (180, -270, .6), (420, -40, 1.6)]))
    def mug(x, col, col2, flip):
        sx = -1 if flip else 1
        return (f'<g transform="translate({x},0) scale({sx},1)">'
                f'<path d="M96 -200 C170 -200 170 -90 96 -90" fill="none" stroke="{col2}" stroke-width="26"/>'
                f'<path d="M-110 -250 L110 -250 L98 -18 Q96 0 76 0 L-76 0 Q-96 0 -98 -18Z" fill="{col}" filter="url(#soft)"/>'
                f'<ellipse cx="0" cy="-250" rx="110" ry="22" fill="{col2}"/><ellipse cx="0" cy="-248" rx="94" ry="15" fill="#7A4A3A"/>'
                f'<path d="M-30 -300 C-60 -340 0 -360 -30 -400 M30 -300 C0 -340 60 -360 30 -410" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".7"/></g>')
    o['mugs'] = '<ellipse cx="0" cy="0" rx="360" ry="26" fill="#22103F" opacity=".15"/>' + mug(-170, '#F28DB2', '#E8628F', False) + mug(170, '#B48CF0', '#7A45B5', True)
    o['candle'] = (grad('mat', [(0, '#C3A8EA'), (1, '#7A45B5')]) + grad('cd', [(0, '#FFF8EC'), (1, '#F1DCC6')]) +
                   '<radialGradient id="fl"><stop offset="0" stop-color="#FFE9B0" stop-opacity=".9"/><stop offset="1" stop-color="#FFB76B" stop-opacity="0"/></radialGradient>'
                   '<rect x="-420" y="-120" width="440" height="120" rx="60" fill="url(#mat)" filter="url(#soft)"/>'
                   '<circle cx="-40" cy="-60" r="60" fill="#9A73D6"/><circle cx="-40" cy="-60" r="40" fill="none" stroke="#6233A0" stroke-width="6"/><circle cx="-40" cy="-60" r="18" fill="none" stroke="#6233A0" stroke-width="6"/>'
                   '<g transform="translate(230,0)"><circle cx="0" cy="-330" r="170" fill="url(#fl)"/>'
                   '<rect x="-80" y="-250" width="160" height="250" rx="16" fill="url(#cd)" filter="url(#soft)"/>'
                   '<ellipse cx="0" cy="-250" rx="80" ry="14" fill="#F6E7D4"/><rect x="-4" y="-286" width="8" height="38" fill="#3E1C6C"/>'
                   '<path d="M0 -380 C30 -340 26 -300 0 -284 C-26 -300 -30 -340 0 -380Z" fill="#FFC86B"/><path d="M0 -350 C12 -330 10 -306 0 -296 C-10 -306 -12 -330 0 -350Z" fill="#FFF3D0"/></g>')
    o['milk'] = (grad('bt', [(0, '#FFFFFF'), (1, '#EEE6F6')]) +
                 '<ellipse cx="0" cy="0" rx="380" ry="24" fill="#22103F" opacity=".18"/>'
                 '<path d="M-200 -440 L-120 -440 L-110 -380 C-60 -350 -60 -320 -60 -280 L-60 -14 Q-60 0 -76 0 L-244 0 Q-260 0 -260 -14 L-260 -280 C-260 -320 -260 -350 -210 -380Z" fill="url(#bt)" filter="url(#soft)"/>'
                 '<rect x="-206" y="-476" width="92" height="44" rx="10" fill="#E8628F"/><rect x="-250" y="-250" width="180" height="110" rx="14" fill="#F7B6CD"/>'
                 '<path d="M-232 -196 C-210 -222 -190 -222 -160 -196 C-130 -170 -110 -170 -88 -196" stroke="#FFF8EC" stroke-width="8" fill="none" stroke-linecap="round"/>'
                 '<path d="M-30 -200 L170 -200 L150 -12 Q148 0 134 0 L6 0 Q-8 0 -10 -12Z" fill="#FFF8EC" filter="url(#soft)"/><rect x="-40" y="-224" width="220" height="30" rx="12" fill="#C3A8EA"/>'
                 '<rect x="16" y="-150" width="110" height="50" rx="10" fill="#E6D6F3"/>'
                 '<g transform="translate(270,-10) rotate(-28)"><path d="M0 0 C-60 -80 -40 -220 40 -290 C110 -220 120 -90 0 0Z" fill="#8FB59B"/><path d="M0 0 C10 -90 20 -180 40 -280" stroke="#5E8A6C" stroke-width="7" fill="none"/>'
                 + ''.join(f'<path d="M{8+k*5} {-60-k*50} C{40+k*4} {-80-k*50} {60} {-110-k*50} {70-k*6} {-120-k*50}" stroke="#5E8A6C" stroke-width="5" fill="none"/>' for k in range(4)) + '</g>')
    o['book'] = (grad('pg', [(0, '#FFF8EC'), (1, '#EFE3D2')]) +
                 '<ellipse cx="0" cy="0" rx="400" ry="26" fill="#000" opacity=".25"/>'
                 '<path d="M0 -40 C-120 -80 -260 -80 -360 -50 L-380 -6 C-260 -36 -120 -30 0 6Z" fill="#4A2070"/>'
                 '<path d="M0 -40 C120 -80 260 -80 360 -50 L380 -6 C260 -36 120 -30 0 6Z" fill="#4A2070"/>'
                 '<path d="M0 -30 C-110 -90 -250 -100 -350 -70 L-330 -270 C-230 -300 -100 -290 0 -230Z" fill="url(#pg)"/>'
                 '<path d="M0 -30 C110 -90 250 -100 350 -70 L330 -270 C230 -300 100 -290 0 -230Z" fill="url(#pg)"/>'
                 + ''.join(f'<path d="M{-300+k*4} {-230+k*36} C-220 {-252+k*36} -110 {-240+k*36} -30 {-200+k*36}" stroke="#7A45B5" stroke-width="5" fill="none" stroke-linecap="round" opacity="{.8 if k<4 else .25}"/>' for k in range(5))
                 + '<rect x="40" y="-330" width="26" height="150" fill="#E8628F" transform="rotate(8)"/>'
                 '<g transform="translate(140,-110) rotate(-24)"><rect x="0" y="0" width="300" height="26" rx="4" fill="#C3A8EA"/><path d="M0 0 L-56 13 L0 26Z" fill="#F3D9B5"/><path d="M-38 9 L-56 13 L-38 17Z" fill="#22103F"/><rect x="300" y="0" width="40" height="26" rx="8" fill="#F28DB2"/></g>')
    return o


def build_fmt(fmt):
    f = FMT[fmt]; W, H = f['W'], f['H']; PW = W * N
    ground = H - (290 if fmt == 1440 else 500)          # where objects stand
    svg = K.DEFS
    OB = objects()
    # hills with a horizontal colour sweep through the week
    st1 = ''.join(f'<stop offset="{(k+0.5)/N:.3f}" stop-color="{c}"/>' for k, c in enumerate(HILL))
    st2 = ''.join(f'<stop offset="{(k+0.5)/N:.3f}" stop-color="{c}"/>' for k, c in enumerate(HILL2))
    svg += f'<linearGradient id="h1" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{PW}" y2="0">{st1}</linearGradient>'
    svg += f'<linearGradient id="h2" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{PW}" y2="0">{st2}</linearGradient>'
    svg += K.hills(PW, H, ground - 150, 60, seed=0.7, fill='url(#h1)', op=.85, waves=(0.0011, 0.0027, 0.0063))
    svg += K.hills(PW, H, ground + 10, 26, seed=2.9, fill='url(#h2)', op=1, waves=(0.0009, 0.0021, 0.0051))
    cells = ''
    # sun path (canvas) positions per slide: (x, y, r)
    gy = ground - 150
    sun = [(1 * W + 0.86 * W, gy - 10, 100), (2 * W + 0.20 * W, H * 0.30 if fmt == 1440 else H * 0.27, 92)]
    # slide 1: seven windows, one per day
    ww, gap = 118, 12
    tot = 7 * ww + 6 * gap
    x0 = (W - tot) / 2
    wy = (f['T'] + 40)
    wh = 260
    for k in range(7):
        x = x0 + k * (ww + gap)
        pal = SKY[k + 1]
        gid = f'win{k}'
        svg += grad(gid, [(0, pal[0]), (0.45, pal[2]), (1, pal[4])])
        svg += (f'<path d="M{x},{wy+wh} L{x},{wy+ww/2} A{ww/2},{ww/2} 0 0 1 {x+ww},{wy+ww/2} L{x+ww},{wy+wh} Z" fill="url(#{gid})" stroke="#FFF8EC" stroke-opacity=".55" stroke-width="3"/>')
        # the sun / moon inside each window
        sy = [0.86, 0.55, 0.32, 0.36, 0.78, 0.9, 0.3][k]
        if k < 5:
            svg += f'<circle cx="{x+ww/2}" cy="{wy+wh*sy}" r="16" fill="#FFF0C9"/>'
        elif k == 6:
            svg += K.moon_phase(x + ww / 2, wy + wh * sy, 15, 'wane', glow=False)
        lab = ['M', 'T', 'W', 'T', 'F', 'S', 'S'][k]
        cells += f'<p class="lab abs" style="left:{x}px;top:{wy+wh+18}px;width:{ww}px;text-align:center;font-size:40px;letter-spacing:0;color:var(--cream)">{lab}</p>'
    cells += cell(0, fmt, f'''<div style="height:{wh+130}px"></div>
        <p class="lab" style="font-size:44px;color:var(--pink);text-align:center;letter-spacing:.12em">Self Care Week.<br>16 to 22 November.</p>
        <h1 class="h" style="font-size:{146 if fmt==1440 else 140}px;text-align:center;margin-top:34px">7 days.<br>7 <em>small</em><br>things.</h1>''')
    # day slides
    for (i, day, date, text, obj, al, dark_text) in DAYS:
        col = INKC if dark_text else 'var(--cream)'
        emc = 'var(--rose)' if dark_text else 'var(--pink)'
        ta = al
        cells += cell(i, fmt, f'''
          <div style="display:flex;align-items:flex-end;gap:26px;flex-direction:{'row' if al=='left' else 'row-reverse'}">
            <span class="h" style="font-size:250px;line-height:.78;color:{col};font-weight:800">{date}</span>
            <span class="lab" style="font-size:52px;color:{emc};letter-spacing:.2em;margin-bottom:6px">{day}</span>
          </div>
          <h2 class="h" style="font-size:{104 if len(text) < 50 else 94}px;color:{col};text-align:{ta};margin-top:44px;max-width:900px;{'align-self:flex-end' if al=='right' else ''}">{text.replace('<em>', f'<em style="color:{emc}">')}</h2>''')
        ox = i * W + (W * 0.70 if al == 'left' else W * 0.30)
        if obj in ('path',):
            ox = i * W + W * 0.62
        if obj == 'milk':
            ox = i * W + W * 0.38
        sc = 0.95 if fmt == 1440 else 0.95
        svg += f'<g transform="translate({ox:.0f},{ground+30}) scale({sc})">{OB[obj]}</g>'
    # last slide
    i = 8
    lw = 600
    cells += lockup(i, fmt, W / 2, f['T'] + 40, lw, center=True)
    cells += cell(i, fmt, f'''<div style="height:{lw*0.44+110}px"></div>
        <h2 class="h" style="font-size:124px;text-align:center">Save this<br>for the <em>week.</em></h2>''')
    for k in range(N - 1):
        cells += chrome(k, N, fmt)
    cells += f'<p class="src" style="left:{8*W+f["L"]}px;bottom:{f["sb"]}px;width:{W-f["L"]-f["R"]}px;text-align:center">Ideas from NHS advice on menopause and perimenopause</p>'
    js = f"""const SKY={json.dumps(SKY)}; const GROUND={ground};
    function fillSky(pal,x,w){{ const g=c.createLinearGradient(0,0,0,H); [0,.36,.66,.86,1].forEach((p,k)=>g.addColorStop(p,pal[k])); c.fillStyle=g; c.fillRect(x,0,w,H); }}
    function draw(){{
      for(let i=0;i<N;i++) fillSky(SKY[i], i*W, W);
      const BW=320;
      for(let i=1;i<N;i++){{ const b=i*W; fillSky(SKY[i-1], b-BW, 2*BW);
        const o=document.createElement('canvas'); o.width=2*BW; o.height=H; const k=o.getContext('2d');
        const g=k.createLinearGradient(0,0,0,H); [0,.36,.66,.86,1].forEach((p,j)=>g.addColorStop(p,SKY[i][j])); k.fillStyle=g; k.fillRect(0,0,2*BW,H);
        k.globalCompositeOperation='destination-in'; const m=k.createLinearGradient(0,0,2*BW,0); m.addColorStop(0,'rgba(0,0,0,0)'); m.addColorStop(1,'rgba(0,0,0,1)'); k.fillStyle=m; k.fillRect(0,0,2*BW,H);
        c.drawImage(o,b-BW,0); }}
      // stars only at night (left of slide 1, and from Saturday on)
      const so=document.createElement('canvas'); so.width=PW; so.height=H; const sk=so.getContext('2d');
      CLARI.stars(sk,PW,H,0.3,{{seed:21,n:1300,bottom:0.62,alpha:0.9,sparkles:26}});
      sk.globalCompositeOperation='destination-in'; const m=sk.createLinearGradient(0,0,PW,0);
      m.addColorStop(0,'rgba(0,0,0,1)'); m.addColorStop(0.9/N,'rgba(0,0,0,.8)'); m.addColorStop(1.25/N,'rgba(0,0,0,0)'); m.addColorStop(6.1/N,'rgba(0,0,0,0)'); m.addColorStop(6.8/N,'rgba(0,0,0,.7)'); m.addColorStop(1,'rgba(0,0,0,1)');
      sk.fillStyle=m; sk.fillRect(0,0,PW,H); c.drawImage(so,0,0);
      // the sun across the week, then the moon
      const suns=[[1.22,GROUND-175,96],[2.80,GROUND-330,82],[3.20,GROUND-420,80],[4.82,GROUND-380,80],[5.24,GROUND-150,124]];
      suns.forEach(([u,y,r])=>{{ const x=u*W; const g=c.createRadialGradient(x,y,r*0.4,x,y,r*4); g.addColorStop(0,'rgba(255,236,190,0.55)'); g.addColorStop(1,'rgba(255,236,190,0)'); c.fillStyle=g; c.fillRect(x-r*4,y-r*4,r*8,r*8);
        const d=c.createRadialGradient(x-r*0.3,y-r*0.3,r*0.1,x,y,r); d.addColorStop(0,'#FFFBEA'); d.addColorStop(1,'#FFD9A0'); c.fillStyle=d; c.beginPath(); c.arc(x,y,r,0,Math.PI*2); c.fill(); }});
      CLARI.moon(c, 7*W+W*0.22, GROUND-360, 84, {{glow:1}});
      CLARI.branch(c, 9*W+30, -20, 2.6, true, 0, {{}});
      CLARI.branch(c, 8*W-40, -20, 2.2, false, 0, {{blossoms:5}});
    }}"""
    return page(TITLE, fmt, N, cells, js=js, svg=svg)


if __name__ == '__main__':
    import sys
    fmts = [int(a) for a in sys.argv[1:]] or [1440, 1920]
    jobs, allouts = [], {}
    for fm in fmts:
        j, outs = build('c3', 'c3', N, fm, build_fmt(fm)); jobs.append(j); allouts[fm] = outs
    render('c3', jobs)
    for fm, outs in allouts.items():
        sheet(outs, f'{S}/c3/sheet_{fm}.jpg')
