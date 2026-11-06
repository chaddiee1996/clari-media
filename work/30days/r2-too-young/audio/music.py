# R2 "Too young?": calm, confident nylon guitar fingerpicking in A minor, 84 bpm, soft cello, very sparse under the voice.
# Arc: guitar alone under the hook, cello enters with the first card, a lift to C major on "too young isn't the end".
import sys, math; sys.path.insert(0, '/home/claude/clari-media/work/kit/music'); sys.path.insert(0, '.')
from musiclib import Song, GM, NOTE, chord, loudness
import sfxlib as fx

BPM = 84; b = lambda s: s * BPM / 60.0
D = 32.2
s = Song(bpm=BPM)
s.inst(0, GM['nylon_guitar'], vol=96, pan=58, reverb=70)
s.inst(1, GM['cello'], vol=78, pan=70, reverb=90)
s.inst(2, GM['pad_warm'], vol=50, reverb=110, chorus=50)

# bars of 4 beats; voicings as [bass, mid, top, top2]
V = {
    'Am': ['A2', 'E3', 'A3', 'C4'], 'Fmaj7': ['F2', 'C3', 'E3', 'A3'], 'C': ['C3', 'G3', 'C4', 'E4'], 'G': ['G2', 'D3', 'G3', 'B3'],
    'Dm': ['D3', 'A3', 'D4', 'F4'], 'E': ['E2', 'B2', 'E3', 'G#3'], 'Am9': ['A2', 'E3', 'B3', 'C4'], 'Csus': ['C3', 'G3', 'D4', 'E4'],
    'F': ['F2', 'C3', 'F3', 'A3'], 'G6': ['G2', 'D3', 'E3', 'B3'],
}
# 45 beats ~ 11.3 bars
prog = ['Am', 'Fmaj7', 'Am', 'Fmaj7',     # hook + NICE says
        'C', 'G', 'Am9', 'Fmaj7',          # over 45, 40 to 45
        'Dm', 'E',                          # under 40
        'F', 'G6', 'Csus']                  # too young isn't the end, write it down
for i, name in enumerate(prog):
    bt = i * 4
    if bt >= b(D): break
    bs, m, t1, t2 = [NOTE(n) for n in V[name]]
    lift = bt >= b(25.6)
    pat = [(0, bs, 58), (0.5, t1, 40), (1, m, 42), (1.5, t2, 44), (2, bs + (12 if name in ('E',) else 7) if False else bs, 50), (2.5, t1, 40), (3, m, 40), (3.5, t2, 46 if lift else 40)]
    for o, p, v in pat:
        if bt + o >= b(D) - 1: continue
        s.note(0, bt + o, 1.6, p, v + (6 if lift else 0))
    if lift:
        s.chord(2, bt, 4.05, [p + 12 for p in (bs, m, t1)], vel=40)
# cello: enters with the first card (7.55 s), long notes, a small line at the lift
cel = [(b(7.6), 'A2', 4.5), (b(7.6) + 4.5, 'C3', 3.5), (b(16.4), 'E3', 4), (b(16.4) + 4, 'D3', 3.5), (b(21.0), 'D3', 3.8), (b(21.0) + 3.8, 'E3', 3.6),
       (b(25.7), 'F3', 2), (b(25.7) + 2, 'A3', 2), (b(25.7) + 4, 'G3', 3), (b(25.7) + 7, 'E3', 2), (b(25.7) + 9, 'C3', 5)]
s.swell(1, b(7.4), 3, 30, 100)
for bt, n, d in cel: s.note(1, bt, d, n, 52)
s.render('bed.wav', seconds=D + 0.2, fade_out=1.6, gain=0.7)

tr = fx.Track(D + 0.2)
tr.add_wav(0, 'bed.wav', 1.0)
def slide(t, g=0.10, d=0.55, pan=0.0): tr.add(t, fx.sweep_noise(d, 1400, 4200, width=0.9, a=0.25, r=0.7), g, pan)
for t in (6.1, 6.35, 7.55, 16.45, 20.95, 28.35): slide(t)
slide(25.6, 0.12, 0.8)
for t0, t1 in ((0.32, 1.05), (2.6, 3.6), (9.6, 10.5), (10.62, 11.35), (17.78, 18.45), (22.5, 23.25), (24.05, 24.5), (28.86, 30.38)):
    tr.add(t0, fx.scratch(t1 - t0 + 0.05, rate=11), 0.07, 0.3)
tr.write('music_sfx.wav', D)
print('bed', loudness('bed.wav'), 'music+sfx', loudness('music_sfx.wav'))
