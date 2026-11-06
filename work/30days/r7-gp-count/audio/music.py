# R7: soft piano ostinato in C major, 96 bpm, light shaker, strings enter on step 3. Under the voice.
import sys, os, subprocess
sys.path.insert(0, '/home/claude/clari-media/work/kit/music'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from musiclib import Song, GM, chord, NOTE, loudness
import sfx, numpy as np
BPM = 96; BT = 60 / BPM; DUR = 26.6
VO = '/home/claude/clari-media/work/30days/vo/R7.mp3'
s = Song(bpm=BPM)
s.inst(0, GM['grand_piano'], vol=88, pan=58, reverb=70)
s.inst(1, GM['strings_slow'], vol=80, pan=70, reverb=95)
s.inst(2, GM['acoustic_bass'], vol=70, reverb=40)
s.inst(3, GM['grand_piano'], vol=70, pan=76, reverb=85)
s.inst(9, 0, vol=70, reverb=30, kit='standard')
b = lambda sec: sec / BT
# hook: urgent high staccato pulse on C, speeding the eye with the stopwatch, stopping dead on "count"
stop = b(3.34)
x = 0.0
while x < stop - 0.2:
    s.note(0, x, 0.2, 'C6', 52); s.note(0, x, 0.2, 'G5', 40); x += 0.5
s.chord(0, stop, 3.0, chord('F4', 'maj7'), vel=50)    # held breath after the stop
# steady ostinato from card 1 (4.55 s): C | Am | F | G, two bars each step
start = b(4.55)
prog = [('C4', 'add9'), ('A3', 'min7'), ('F3', 'maj7'), ('G3', 'sus4'), ('C4', 'add9'), ('A3', 'min7'), ('F3', 'maj7'), ('G3', 'maj'),
        ('A3', 'min7'), ('F3', 'maj7'), ('C4', 'maj'), ('G3', 'sus4'), ('F3', 'maj7'), ('G3', 'maj')]
basses = ['C2', 'A1', 'F1', 'G1', 'C2', 'A1', 'F1', 'G1', 'A1', 'F1', 'C2', 'G1', 'F1', 'G1']
close = b(23.74)
bar = 0; t0 = start
while t0 < close - 0.1 and bar < len(prog):
    r, k = prog[bar]; ps = chord(r, k)
    patt = [ps[0], ps[2], ps[1] + 12, ps[2], ps[0] + 12, ps[2], ps[1] + 12, ps[2]]
    for j, p in enumerate(patt):
        if t0 + j * 0.5 < close: s.note(0, t0 + j * 0.5, 0.45, p, 44 + (8 if j % 4 == 0 else 0))
    s.note(2, t0, 3.9, basses[bar], 58)
    if t0 >= b(17.45) - 0.01: s.chord(1, t0, 4.0, [p + 12 for p in ps[:3]], vel=46)
    for j in range(8):
        if t0 + j * 0.5 < close: s.drum(t0 + j * 0.5, 'shaker', 22 + (10 if j % 2 else 0))
    t0 += 4; bar += 1
s.swell(1, b(17.45), 4, 30, 100)
# close: C add9, a little melody answers "Save this"
s.chord(0, close, 6, chord('C4', 'add9'), vel=54, strum=0.04); s.note(2, close, 6, 'C2', 60)
s.chord(1, close, 6, chord('C5', 'maj'), vel=48)
for j, n in enumerate(['E5', 'G5', 'D6', 'C6']): s.note(3, close + 1 + j * 0.75, 2, n, 50)
s.render('bed.wav', seconds=DUR, fade_out=2.2, gain=0.7)
# sfx
N = int(DUR * sfx.SR); fx = np.zeros((N, 2), np.float32)
tt = 0.0
while tt < 3.3:   # ticks accelerate with the hand
    sfx.place(fx, sfx.tick(seed=int(tt * 100), f=3400), tt, 0.5); tt += max(0.07, 0.24 - tt * 0.05)
sfx.place(fx, sfx.clunk(seed=2, f=520), 3.32, 0.4); sfx.place(fx, sfx.tick(seed=9, f=2200), 3.32, 0.8)
for k, t in enumerate((4.55, 11.85, 17.45)): sfx.place(fx, sfx.slide(0.5, seed=30 + k), t, 0.7); sfx.place(fx, sfx.clunk(seed=k, f=140), t + 0.42, 0.25)
sfx.place(fx, sfx.whoosh(0.7, seed=44), 13.4, 0.25); sfx.place(fx, sfx.slide(0.7, seed=50), 23.4, 0.5)
sfx.write('fx.wav', fx)
# VO -16 LUFS, starts at 0
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', VO, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', '-ac', '2', 'vo.wav'], check=True)
pad = lambda x: np.pad(x, ((0, max(0, N - len(x))), (0, 0)))[:N]
vo, bed = pad(sfx.read('vo.wav')), pad(sfx.read('bed.wav'))
# set music+fx so its loudness sits ~12 dB under the VO
music = bed + fx * 0.8
sfx.write('music_tmp.wav', music); Lm = loudness('music_tmp.wav'); Lv = loudness('vo.wav')
g = 10 ** (((Lv - 12) - Lm) / 20); music *= g
sfx.write('music_set.wav', music)
sfx.write('mix.wav', vo + music)
print('vo', Lv, 'music', loudness('music_set.wav'), 'mix', loudness('mix.wav'))
# trim the whole mix so the voice sits at -16 LUFS (single-pass loudnorm lands a touch low on short speech)
G = 10 ** ((-16 - Lv) / 20)
sfx.write('mix_g.wav', (vo + music) * G)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'mix_g.wav', '-af', 'alimiter=limit=0.89:level=false', 'mix.wav'], check=True)
sfx.write('vo_g.wav', vo * G); print('vo final', loudness('vo_g.wav'), 'mix final', loudness('mix.wav'))
