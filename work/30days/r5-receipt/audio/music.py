# R5 The receipt: lo-fi Rhodes + finger bass + brushed kit, B flat major, 82 bpm.
# Arc: Rhodes alone while the header prints, groove from item 1, a hit on TOTAL, the kit drops out at the tear,
# Eb major 9 opens on "imagining", B flat add9 resolves on "Keep the receipt", tail into the sting.
import sys, os, subprocess
sys.path.insert(0, '/home/claude/clari-media/work/kit/music'); sys.path.insert(0, os.path.dirname(__file__))
from musiclib import Song, GM, chord, NOTE, loudness
import sfx
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BPM = 82; B = 60 / BPM; DUR = 23.1
s = Song(bpm=BPM)
s.inst(0, GM['rhodes'], vol=92, pan=56, reverb=70, chorus=40)      # chords
s.inst(1, GM['rhodes'], vol=100, pan=72, reverb=80, chorus=30)     # melody
s.inst(2, GM['finger_bass'], vol=104, pan=64, reverb=20)
s.inst(9, 0, vol=86, reverb=40, kit='brush')
# bars of 4 beats: chord per bar (TOTAL lands at beat 16.5, tear at 22.5)
prog = [('Bb3', 'maj7'), ('G3', 'min9'), ('Eb3', 'maj7'), ('F3', 'sus4'),
        ('Bb3', 'maj7'), ('G3', 'min9')]
for i, (r, k) in enumerate(prog):
    b = i * 4
    v = 52 if i == 0 else 58
    s.chord(0, b, 3.9, chord(r, k), vel=v, strum=0.03)
    if i in (1, 2, 3, 4, 5):  # lazy upbeat re-voicing, lo-fi
        s.chord(0, b + 2.5, 1.4, chord(r, k)[1:], vel=v - 14, strum=0.02)
# F7 turnaround inside bar 4
s.chord(0, 14, 1.9, chord('F3', '7'), vel=54, strum=0.03)
# TOTAL hit: Eb major 7 stab on 16.5 with bass
s.chord(0, 16.5, 1.6, chord('Eb3', 'maj9'), vel=72, strum=0.015)
# after the tear: open, no drums
s.chord(0, 23.5, 4.0, chord('Eb3', 'maj9'), vel=60, strum=0.05)
s.chord(0, 27.5, 5.0, chord('Bb3', 'add9'), vel=58, strum=0.06)
s.note(0, 27.5, 5.0, 'D3', 50)
# bass (finger bass, root-fifth, laid back)
bass = [(0, 'Bb1', 0), (4, 'G1', 1), (8, 'Eb2', 1), (12, 'F1', 1), (16, 'Bb1', 1), (20, 'G1', 1)]
for b, n, on in bass:
    if not on: continue
    p = NOTE(n)
    s.note(2, b, 1.4, p, 88); s.note(2, b + 1.5, 0.45, p + 7, 70); s.note(2, b + 2.5, 1.2, p + 12 if b != 12 else p + 10, 74)
    s.note(2, b + 3.5, 0.45, p + 7, 64)
s.note(2, 16.5, 1.4, 'Eb2', 96)
s.note(2, 22.5, 1.0, 'F1', 70)
s.note(2, 23.5, 4.0, 'Eb2', 80); s.note(2, 27.5, 4.5, 'Bb1', 84)
# brushed kit from item 1 (beat 1.5) to the tear (22.5)
for b8 in range(0, 45):
    b = b8 * 0.5
    if b < 4 or b >= 22.5: continue
    sw = 0.08 if b8 % 2 else 0      # swing the offbeats
    s.drum(b + sw, 'hat', 34 + (8 if b8 % 2 == 0 else 0))
    if b % 4 in (0.0,) or b % 4 == 2.5: s.drum(b, 'kick', 70)
    if b % 4 in (1.0, 3.0): s.drum(b, 'snare', 46)
s.drum(16.5, 'kick', 92); s.drum(16.5, 'crash', 40)
# light hats during the intro so it is not empty
for b in (1.5, 2.0, 2.5, 3.0, 3.5): s.drum(b, 'hat', 26)
# melody: a lazy, sighing line in the gaps between punchlines (B flat pentatonic)
mel = [(2.6, 'F5', 0.4), (3.0, 'D5', 0.4), (3.4, 'C5', 1.0),
       (6.6, 'F5', 0.4), (7.0, 'G5', 0.4), (7.4, 'F5', 0.4), (7.8, 'D5', 1.2),
       (10.6, 'Eb5', 0.4), (11.0, 'D5', 0.4), (11.4, 'Bb4', 1.2),
       (14.6, 'C5', 0.4), (15.0, 'D5', 0.4), (15.4, 'F5', 1.0),
       (18.6, 'G5', 0.5), (19.1, 'F5', 0.5), (19.6, 'D5', 1.4),
       (24.0, 'G5', 0.8), (25.0, 'F5', 0.8), (26.0, 'D5', 1.6),
       (28.0, 'F5', 0.6), (28.7, 'D5', 0.6), (29.4, 'C5', 0.6), (30.1, 'D5', 2.0)]
for b, n, d in mel: s.note(1, b, d, n, 62)
s.render('bed_raw.wav', seconds=DUR + 1.0, fade_out=2.0, gain=0.7)
# lo-fi: gentle tape wobble + top roll-off
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'bed_raw.wav', '-af',
                'vibrato=f=0.7:d=0.04,lowpass=f=7500,highpass=f=40', '-ar', '48000', 'bed.wav'], check=True)

# glockenspiel till beeps (one per item, one on TOTAL)
g = Song(bpm=BPM); g.inst(0, GM['glockenspiel'], vol=100, reverb=50)
for i in range(5): g.note(0, 1.5 + 3 * i, 0.3, 'B6', 70)
g.note(0, 16.5, 0.4, 'B6', 82); g.note(0, 16.5, 0.4, 'F#6', 60)
g.render('beeps.wav', seconds=DUR + 1.0, fade_out=0.5, gain=0.6)

# printer bursts at every feed (same times as the picture's rows)
ITEMS_A = [2, 1, 1, 1, 1]; ITEMS_B = [1, 1, 1, 1, 2]
feeds = [(0.12, 0.30), (0.34, 0.30), (0.56, 0.2)]
for i in range(5):
    t0 = 1.5 * B + 3 * B * i
    feeds.append((t0, 0.22 + 0.15 * ITEMS_A[i])); feeds.append((t0 + 1.5 * B, 0.22 + 0.15 * ITEMS_B[i]))
for b in (16.5, 17, 17.5, 18, 19.5, 20, 20.5): feeds.append((b * B, 0.34 if b != 20.5 else 0.5))
n = int((DUR + 1) * sfx.SR); fx = np.zeros((n, 2), np.float32)
for k, (t, d) in enumerate(feeds): sfx.place(fx, sfx.printer(d, seed=k), t - 0.01, 0.4)
T_TEAR = 22.5 * B
sfx.place(fx, sfx.tear(0.5), T_TEAR - 0.28, 0.9)
for k, dt in enumerate((1.0, 1.45, 1.9)): sfx.place(fx, sfx.clunk(seed=k, f=90 - 8 * k), T_TEAR + dt, 0.35)
sfx.place(fx, sfx.whoosh(1.4, seed=11, lo=200, hi=1600, peak_at=0.4), T_TEAR + 0.05, 0.25)
sfx.write('fx.wav', fx)

bed = sfx.read('bed.wav'); bp_ = sfx.read('beeps.wav')
N = int(DUR * sfx.SR)
pad = lambda x: np.pad(x, ((0, max(0, N - len(x))), (0, 0)))[:N]
mix = pad(bed) * 1.0 + pad(bp_) * 0.55 + pad(fx) * 0.9
mix = mix[:int(DUR * sfx.SR)]
sfx.write('mix_pre.wav', mix)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'mix_pre.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9',
                '-ar', '48000', '-ac', '2', 'mix.wav'], check=True)
print('bed', loudness('bed.wav'), 'mix', loudness('mix.wav'))
