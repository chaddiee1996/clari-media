# R8: hushed, intimate. Warm pad + celesta in A flat major, 72 bpm, soft heartbeat kick. Under the voice.
import sys, os, subprocess
sys.path.insert(0, '/home/claude/clari-media/work/kit/music'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from musiclib import Song, GM, chord, NOTE, loudness
import sfx, numpy as np
BPM = 72; BT = 60 / BPM; DUR = 17.9
VO = '/home/claude/clari-media/work/30days/vo/R8.mp3'
b = lambda sec: sec / BT
s = Song(bpm=BPM)
s.inst(0, GM['pad_warm'], vol=84, reverb=100, chorus=60)
s.inst(1, GM['celesta'], vol=96, pan=70, reverb=100)
s.inst(2, GM['fretless_bass'], vol=64, reverb=50)
s.inst(3, GM['strings_slow'], vol=60, pan=50, reverb=100)
s.inst(9, 0, vol=80, reverb=20, kit='room')
# Ab | Fm7 | Db maj7 | Eb sus4, the lock lands on Ab add9 (14.9 s)
prog = [('Ab3', 'add9'), ('F3', 'min7'), ('Db3', 'maj7'), ('Eb3', 'sus4'), ('Ab3', 'add9'), ('F3', 'min9'), ('Db3', 'maj9')]
bass = ['Ab1', 'F1', 'Db2', 'Eb2', 'Ab1', 'F1', 'Db2']
for i, ((r, k), bn) in enumerate(zip(prog, bass)):
    st = i * 4
    if b(14.9) <= st: break
    s.chord(0, st, 4.1, chord(r, k), vel=56); s.note(2, st, 3.8, bn, 56)
lock = b(14.9)
s.chord(0, lock, 6, chord('Ab3', 'add9'), vel=62); s.note(2, lock, 6, 'Ab1', 60)
s.chord(3, lock, 6, chord('Ab4', 'maj'), vel=52); s.swell(3, lock, 2, 30, 100)
# heartbeat: lub-dub on beat 1 of every bar from the phone's rise, very soft
for st in range(int(b(3.0)) // 4 * 4 + 4, int(lock), 4):
    s.drum(st, 'kick', 52); s.drum(st + 0.35, 'kick', 36)
s.drum(lock, 'kick', 60); s.drum(lock + 0.35, 'kick', 40)
# celesta: sparse falling figure in the voice gaps (Ab pentatonic), a brighter rise on the lock
for sec, n in [(2.9, 'Eb6'), (3.25, 'C6'), (3.6, 'Ab5'), (6.6, 'F6'), (6.9, 'Eb6'), (8.6, 'C6'), (8.85, 'Bb5'), (11.0, 'Eb6'), (11.25, 'C6'), (14.6, 'Ab5')]:
    s.note(1, b(sec), 1.6, n, 56)
for j, n in enumerate(['Ab5', 'C6', 'Eb6', 'Ab6']): s.note(1, lock + 0.25 + j * 0.4, 3, n, 60 - j * 4)
s.render('bed.wav', seconds=DUR, fade_out=2.0, fade_in=0.4, gain=0.7)
N = int(DUR * sfx.SR); fx = np.zeros((N, 2), np.float32)
for i in range(4): sfx.place(fx, sfx.whoosh(1.2, seed=60 + i, lo=250, hi=2200, peak_at=0.6), 3.7 + i * 0.55, 0.32)
sfx.place(fx, sfx.whoosh(1.4, seed=70, lo=150, hi=900, peak_at=0.7), 14.9, 0.4)
sfx.place(fx, sfx.clunk(seed=5, f=180), 15.95, 0.3)
sfx.write('fx.wav', fx)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', VO, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', '-ac', '2', 'vo.wav'], check=True)
pad = lambda x: np.pad(x, ((0, max(0, N - len(x))), (0, 0)))[:N]
vo, bed = pad(sfx.read('vo.wav')), pad(sfx.read('bed.wav'))
music = bed + fx * 0.8
sfx.write('music_tmp.wav', music); Lm = loudness('music_tmp.wav'); Lv = loudness('vo.wav')
music *= 10 ** (((Lv - 12) - Lm) / 20)
G = 10 ** ((-16 - Lv) / 20)
sfx.write('vo_g.wav', vo * G); sfx.write('music_set.wav', music * G); sfx.write('mix_g.wav', (vo + music) * G)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'mix_g.wav', '-af', 'alimiter=limit=0.89:level=false', 'mix.wav'], check=True)
print('vo', loudness('vo_g.wav'), 'music', loudness('music_set.wav'), 'mix', loudness('mix.wav'))
