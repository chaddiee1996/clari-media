# R6 Not a bubble bath: harp + slow strings, G major, 70 bpm in 3/4, celesta on each bubble.
# Arc: harp alone under the hook, strings enter with bubble 1, swell to bubble 6, lift (G add9, bright) on the pops.
import sys, os, subprocess
sys.path.insert(0, '/home/claude/clari-media/work/kit/music'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from musiclib import Song, GM, chord, NOTE, loudness
import sfx, numpy as np
BPM = 70; BT = 60 / BPM; BAR = 3 * BT; DUR = 23.14; T_POP = 7 * BAR
s = Song(bpm=BPM)
s.inst(0, GM['harp'], vol=100, pan=50, reverb=85)
s.inst(1, GM['strings_slow'], vol=78, pan=70, reverb=95, chorus=30)
s.inst(2, GM['celesta'], vol=100, pan=64, reverb=95)
s.inst(3, GM['contrabass'], vol=70, pan=64, reverb=60)
prog = [('G3', 'add9'), ('E3', 'min7'), ('C3', 'maj7'), ('D3', 'sus4'), ('B2', 'min7'), ('A2', 'min7'), ('C3', 'maj7'), ('G3', 'add9'), ('E3', 'min7'), ('G3', 'add9')]
bass = ['G2', 'E2', 'C2', 'D2', 'B1', 'A1', 'C2', 'G1', 'E2', 'G1']
for i, ((r, k), bn) in enumerate(zip(prog, bass)):
    b = i * 3
    ps = chord(r, k)
    # harp: rising broken chord in eighths, two octaves
    arp = [ps[0], ps[1], ps[2], ps[0] + 12, ps[1] + 12, ps[2] + 12] if i < 9 else [ps[0], ps[2], ps[1] + 12]
    for j, p in enumerate(arp): s.note(0, b + j * 0.5, 1.6, p, 58 + (8 if j == 0 else 0) + (6 if i == 7 else 0))
    if i == 3: s.note(0, b + 2.5, 1, NOTE('F#4'), 56)   # sus resolves
    if i >= 1:
        v = 40 + min(6, i) * 5 if i < 7 else 70 - (i - 7) * 10
        s.chord(1, b, 3.05, [p + 12 for p in ps[:3]], vel=v)
        s.note(3, b, 3.0, bn, 54 if i < 7 else 62)
s.swell(1, 3, 3, 40, 100); s.swell(1, 18, 3, 100, 120); s.swell(1, 21, 6, 120, 70)
# celesta: one note per bubble, together they make the tune; the pop answers with the top
mel = ['D6', 'B5', 'E6', 'A5', 'G6', 'F#6']
for i, n in enumerate(mel):
    b = (i + 1) * 3 + 0.25
    s.note(2, b, 2.2, n, 74); s.note(2, b + 1.0, 1.4, NOTE(n) - 5 if i % 2 == 0 else NOTE(n) - 3, 48)
for j, n in enumerate(['G6', 'B6', 'D7', 'G6']): s.note(2, 21 + 0.25 + j * 0.5, 2.5, n, 70 - j * 6)
s.note(2, 24.5, 3, 'B6', 50)
s.render('bed.wav', seconds=DUR + 0.5, fade_out=2.5, gain=0.7)
# sfx: water bed, bloop on each launch, pops at the end
N = int(DUR * sfx.SR); fx = np.zeros((N, 2), np.float32)
w = sfx.water(DUR, level=0.22); fade = np.minimum(1, np.linspace(0, DUR, len(w)) / 1.5)[:, None] * np.clip((DUR - np.linspace(0, DUR, len(w))) / 3, 0, 1)[:, None]
fx[:len(w)] += w * fade * 0.3
for i in range(6):
    t0 = (i + 1) * BAR - 0.35
    sfx.place(fx, sfx.blip(260 + 40 * i, 0.22, 1.4), t0, 0.5)
    sfx.place(fx, sfx.whoosh(1.0, seed=20 + i, lo=250, hi=1500, peak_at=0.35), t0, 0.12)
pops = [T_POP] + [T_POP + 0.14 * (i + 1) for i in range(5)]
for k, t in enumerate(pops): sfx.place(fx, sfx.blip(900 + 160 * k, 0.09, 0.9), t, 0.6)
sfx.write('fx.wav', fx)
bed = sfx.read('bed.wav')
pad = lambda x: np.pad(x, ((0, max(0, N - len(x))), (0, 0)))[:N]
sfx.write('mix_pre.wav', pad(bed) + fx * 0.8)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'mix_pre.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', '-ac', '2', 'mix.wav'], check=True)
print('bed', loudness('bed.wav'), 'fx', loudness('fx.wav'), 'mix', loudness('mix.wav'))
