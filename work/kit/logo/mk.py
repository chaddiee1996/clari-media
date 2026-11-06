import math,random,pathlib
def blossom(cx,cy,s,rot,fillid='pt',center='#E8628F',stamen=True,mono=None):
    pet=''.join(f'<path d="M0 0 C-17 -14 -19 -38 -5 -46 L0 -40 L5 -46 C19 -38 17 -14 0 0Z" fill="{mono or "url(#"+fillid+")"}" transform="rotate({a})"/>' for a in range(0,360,72))
    st='' if (mono or not stamen) else ''.join(f'<line x1="0" y1="0" x2="{18*math.cos(math.radians(a)):.1f}" y2="{18*math.sin(math.radians(a)):.1f}" stroke="#C2457A" stroke-width="2.4"/><circle cx="{18*math.cos(math.radians(a)):.1f}" cy="{18*math.sin(math.radians(a)):.1f}" r="3.6" fill="#FFE29A"/>' for a in range(18,378,36))
    c='' if mono else f'<circle r="9" fill="{center}"/>'
    return f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">{pet}{st}{c}</g>'
DEFS='''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7A45B5"/><stop offset=".55" stop-color="#4A2180"/><stop offset="1" stop-color="#22103F"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#F9C9D8" stop-opacity=".55"/><stop offset=".5" stop-color="#F9C9D8" stop-opacity=".16"/><stop offset="1" stop-color="#F9C9D8" stop-opacity="0"/></radialGradient>
<radialGradient id="moon" cx=".35" cy=".3" r=".85"><stop offset="0" stop-color="#FFFCF2"/><stop offset=".55" stop-color="#FFEFC9"/><stop offset="1" stop-color="#F5C99E"/></radialGradient>
<linearGradient id="pt" x1="0" y1="-46" x2="0" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFF0F5"/><stop offset="1" stop-color="#F28DB2"/></linearGradient>
</defs>'''
def mark(cx,cy,R,mono=None,glow=True):
    # crescent: big circle minus offset circle
    mid=f'cm{random.randint(0,99999)}'
    fill=mono or 'url(#moon)'
    g=f'<circle cx="{cx}" cy="{cy}" r="{R*1.75}" fill="url(#glow)"/>' if (glow and not mono) else ''
    m=f'<mask id="{mid}"><rect width="1024" height="1024" fill="#fff"/><circle cx="{cx+R*0.42}" cy="{cy-R*0.30}" r="{R*0.86}" fill="#000"/></mask>'
    cres=f'{m}<circle cx="{cx}" cy="{cy}" r="{R}" fill="{fill}" mask="url(#{mid})"/>'
    b1=blossom(cx-R*0.18,cy+R*0.55,R/88,12,mono=mono)
    b2=blossom(cx+R*0.38,cy+R*0.70,R/150,40,mono=mono)
    bud='' if mono else f'<ellipse cx="{cx-R*0.62}" cy="{cy+R*0.16}" rx="{R*0.05}" ry="{R*0.07}" fill="#F49BBB" transform="rotate(-20 {cx-R*0.62} {cy+R*0.16})"/>'
    return g+cres+b1+b2+bud
random.seed(4)
stars=''.join(f'<circle cx="{random.uniform(60,964):.0f}" cy="{random.uniform(60,964):.0f}" r="{random.choice([2,2.5,3,4])}" fill="#fff" opacity="{random.uniform(.35,.85):.2f}"/>' for _ in range(28))
sp=lambda x,y,s:f'<path d="M0 -14 Q0 0 14 0 Q0 0 0 14 Q0 0 -14 0 Q0 0 0 -14Z" fill="#FFF6DD" transform="translate({x} {y}) scale({s})"/>'
def svg(body,size=1024): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 1024 1024">{DEFS}{body}</svg>'
files={
 'icon': svg(f'<rect width="1024" height="1024" fill="url(#bg)"/>{stars}{sp(770,250,1.3)}{sp(230,300,1)}{sp(800,760,.8)}'+mark(540,512,300)),
 'adaptive-fg': svg(mark(512,512,205)),  # within 66/108 safe zone: 1024*66/108=626 -> R~205 ok incl glow tolerance
 'adaptive-bg': svg(f'<rect width="1024" height="1024" fill="url(#bg)"/>{stars}'),
 'mono': svg(mark(512,512,205,mono='#000000',glow=False)),
 'splash': svg(mark(512,512,300,glow=True)),
 'notif': svg('<mask id="nm"><rect width="1024" height="1024" fill="#fff"/><circle cx="620" cy="400" r="330" fill="#000"/></mask><circle cx="470" cy="512" r="390" fill="#FFFFFF" mask="url(#nm)"/>'),
}
for k,v in files.items(): pathlib.Path(k+'.svg').write_text(v)
extra={
 'mark': svg(mark(512,512,330,glow=False)),
 'mark-glow': svg(mark(512,512,300,glow=True)),
 'mark-white': svg(mark(512,512,330,mono='#FFFFFF',glow=False)),
 'mark-plum': svg(mark(512,512,330,mono='#4A2070',glow=False)),
}
for k,v in extra.items(): pathlib.Path(k+'.svg').write_text(v)
