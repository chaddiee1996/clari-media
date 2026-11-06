"""Small SVG helpers in the Clari flat-gradient style."""
import math

DEFS = """
<defs>
 <radialGradient id="glowW"><stop offset="0" stop-color="#FFF6DD" stop-opacity=".9"/><stop offset=".35" stop-color="#F9C9D8" stop-opacity=".35"/><stop offset="1" stop-color="#F9C9D8" stop-opacity="0"/></radialGradient>
 <radialGradient id="glowP"><stop offset="0" stop-color="#F9C9D8" stop-opacity=".55"/><stop offset=".5" stop-color="#F9C9D8" stop-opacity=".16"/><stop offset="1" stop-color="#F9C9D8" stop-opacity="0"/></radialGradient>
 <radialGradient id="glowHot"><stop offset="0" stop-color="#FFF3D6" stop-opacity="1"/><stop offset=".18" stop-color="#FFD9A8" stop-opacity=".75"/><stop offset=".45" stop-color="#F59AB8" stop-opacity=".28"/><stop offset="1" stop-color="#E8628F" stop-opacity="0"/></radialGradient>
 <radialGradient id="moonG" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#FFFCF2"/><stop offset=".55" stop-color="#FFEFC9"/><stop offset="1" stop-color="#F5C99E"/></radialGradient>
 <linearGradient id="petalG" x1="0" y1="-46" x2="0" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFF0F5"/><stop offset="1" stop-color="#F28DB2"/></linearGradient>
 <filter id="soft" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#10042A" flood-opacity=".35"/></filter>
 <filter id="softS" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#10042A" flood-opacity=".28"/></filter>
</defs>"""


def sparkle(x, y, s, fill='#FFF6DD', op=1):
    return (f'<path transform="translate({x:.1f},{y:.1f}) scale({s/16:.3f})" fill="{fill}" opacity="{op}" '
            f'd="M0-16Q0 0 16 0Q0 0 0 16Q0 0-16 0Q0 0 0-16Z"/>')


def star(x, y, r=10, glow=46, arms=30, op=1):
    o = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{glow}" fill="url(#glowW)" opacity="{op}"/>'
    if arms:
        o += sparkle(x, y, arms, op=op)
    o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FFF8EC" opacity="{op}"/>'
    return o


def petal_path():
    return 'M0 0C-17-14-19-38-5-46L0-40L5-46C19-38 17-14 0 0Z'


def blossom(x, y, s, rot=0, op=1):
    o = f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({s})" opacity="{op}">'
    for k in range(5):
        o += f'<path transform="rotate({k*72})" fill="url(#petalG)" d="{petal_path()}"/>'
    for k in range(10):
        a = math.radians(18 + 36 * k)
        ex, ey = 18 * math.cos(a), 18 * math.sin(a)
        o += f'<line x1="0" y1="0" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#C2457A" stroke-width="2.4"/><circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.6" fill="#FFE29A"/>'
    o += '<circle r="9" fill="#E8628F"/></g>'
    return o


def petal(x, y, s, rot=0, op=1):
    return f'<path transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({s*0.6})" fill="url(#petalG)" opacity="{op}" d="{petal_path()}"/>'


def hills(pw, h, top, amp, seed=0, fill='#3B1868', op=1, waves=(0.00062, 0.0017, 0.0041)):
    """continuous rolling horizon across the whole panorama."""
    pts = []
    for x in range(0, pw + 41, 40):
        y = top + amp * (0.55 * math.sin(x * waves[0] + seed) + 0.3 * math.sin(x * waves[1] + seed * 2.1) + 0.15 * math.sin(x * waves[2] + seed * 3.7))
        pts.append(f'{x},{y:.1f}')
    return f'<path fill="{fill}" opacity="{op}" d="M0,{h} L{" L".join(pts)} L{pw},{h} Z"/>'


def moon_phase(cx, cy, r, phase, glow=True, gid='moonG', lit='#FFEFC9', dark='rgba(34,16,63,0)'):
    """phase: 'full', 'wax' (lit right), 'wane' (lit left), or float k in -1..1 for crescent cut."""
    o = ''
    if glow:
        o += f'<circle cx="{cx}" cy="{cy}" r="{r*2.4}" fill="url(#glowP)"/>'
    if phase == 'full':
        o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>'
        return o
    mid = f'm{cx}{cy}'.replace('.', '_').replace('-', 'n')
    off = r * 0.62 if phase == 'wax' else -r * 0.62
    o += (f'<mask id="{mid}"><rect x="{cx-r-2}" y="{cy-r-2}" width="{2*r+4}" height="{2*r+4}" fill="#fff"/>'
          f'<circle cx="{cx-off}" cy="{cy}" r="{r*0.92}" fill="#000"/></mask>'
          f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})" mask="url(#{mid})"/>')
    return o
