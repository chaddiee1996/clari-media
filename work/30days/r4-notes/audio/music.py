# R4 "The notes nobody writes": warm Rhodes chords in D major, 76 bpm, brushed snare very low,
# a single harp gliss at the turn ("So write them down"), then the progression resolves on D add9.
import sys; sys.path.insert(0, '/home/claude/clari-media/work/kit/music'); sys.path.insert(0, '.')
from musiclib import Song, GM, NOTE, chord, loudness
import sfxlib as fx

BPM = 76; b = lambda s: s * BPM / 60.0
D = 27.9; TURN = 24.88
s = Song(bpm=BPM)
s.inst(0, GM['rhodes'], vol=96, pan=60, reverb=85, chorus=40)
s.inst(1, GM['rhodes'], vol=80, pan=50, reverb=85)
s.inst(2, GM['harp'], vol=100, pan=74, reverb=100)
s.inst(3, GM['pad_warm'], vol=46, reverb=110, chorus=50)
s.inst(9, 0, vol=70, kit='brush', reverb=50)

prog = [('D4', 'maj9', 'D3'), ('B3', 'min7', 'B2'), ('G3', 'maj7', 'G2'), ('A3', 'sus4', 'A2'),
        ('F#3', 'min7', 'F#2'), ('E3', 'min7', 'E2'), ('G3', 'maj7', 'G2'), ('A3', '7', 'A2'),
        ('G3', 'maj9', 'G2'), ('D4', 'add9', 'D3')]
bt = 0
for i, (r, k, bass) in enumerate(prog):
    if bt >= b(D): break
    dur = 4
    if bt < b(TURN) < bt + 4: dur = b(TURN) - bt       # land the turn on Gmaj9 exactly
    ps = chord(r, k)
    s.chord(0, bt, dur + 0.2, ps, vel=48, strum=0.03)
    if dur > 2.5: s.chord(0, bt + 2, dur - 1.8, ps[1:], vel=36)
    s.note(1, bt, dur + 0.3, bass, 50)
    if bt >= b(TURN) - 0.1: s.chord(3, bt, dur + 2, [p + 12 for p in ps[:3]], vel=44)
    bt += dur
# a few Rhodes melody notes in the gaps between phrases
for t0, n in ((3.9, 'F#5'), (4.4, 'A5'), (9.6, 'E5'), (17.1, 'D5'), (17.5, 'C#5'), (20.2, 'B4'), (24.2, 'A5')):
    s.note(0, b(t0), 1.2, n, 44)
# harp gliss up D major at the turn
gl = ['D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G5', 'A5', 'B5', 'D6']
for i, n in enumerate(gl): s.note(2, b(TURN - 0.55) + i * 0.07, 2.5, n, 62 + i)
# brushes, very low, from the first stat onwards
x = b(5.0)
while x < b(D - 1.5):
    s.drum(x + 1, 'snare2', 24); s.drum(x + 3, 'snare2', 22)
    s.drum(x, 'brush_swirl', 14)
    x += 4
s.render('bed.wav', seconds=D + 0.2, fade_out=1.6, gain=0.7)

tr = fx.Track(D + 0.2)
tr.add_wav(0, 'bed.wav', 1.0)
tr.add(3.2, fx.sweep_noise(0.9, 700, 2600, width=0.8), 0.10, -0.3)   # cover opens
for t0, t1, g in ((6.35, 8.8, 0.03), (9.0, 9.75, 0.07), (25.12, 27.4, 0.07)):
    tr.add(t0, fx.scratch(t1 - t0, rate=12), g, 0.25)
tr.write('music_sfx.wav', D)
print('bed', loudness('bed.wav'), 'music+sfx', loudness('music_sfx.wav'))
