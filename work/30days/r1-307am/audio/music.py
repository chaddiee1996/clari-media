# R1 "3:07am": felt piano lullaby in E flat major, 66 bpm, music box doubling the top line, warm pad.
# Arc: music box alone in the dark (clock), piano enters at the room reveal, strings and warmth at dawn,
# resolves on E flat add9 under the phone. Plus SFX on the picture's moments.
import sys; sys.path.insert(0, '/home/claude/clari-media/work/kit/music'); sys.path.insert(0, '.')
from musiclib import Song, GM, NOTE, chord, loudness
import sfxlib as fx

BPM = 66; b = lambda s: s * BPM / 60.0
s = Song(bpm=BPM)
s.inst(0, GM['felt_piano'], vol=92, pan=60, reverb=80)
s.inst(1, GM['music_box'], vol=80, pan=72, reverb=95)
s.inst(2, GM['pad_warm'], vol=70, reverb=110, chorus=60)
s.inst(3, GM['strings_slow'], vol=78, pan=54, reverb=100)
s.inst(4, GM['felt_piano'], vol=78, pan=50, reverb=80)   # left hand

# music box alone: the clock in the dark (0 to 1.4 s)
for bt, n in ((0.15, 'Bb5'), (0.6, 'G5'), (1.05, 'Eb6')):
    s.note(1, bt, 1.4, n, 70)

# chords, two beats each, from the room reveal (beat 1.6)
prog = [('Eb3', 'maj'), ('Bb2', 'maj'), ('C3', 'min'), ('Ab2', 'maj'), ('F2', 'min7'), ('Bb2', 'sus4'),
        ('Eb3', 'maj'), ('Ab2', 'maj7'), ('F2', 'min7'), ('Bb2', '7'), ('Eb3', 'add9')]
start = 1.6
for i, (root, kind) in enumerate(prog):
    bt = start + i * 2
    if bt > 22: break
    ps = chord(root, kind)
    # lullaby left hand: root, fifth, third, fifth in eighths
    pat = [ps[0], ps[0] + 7, ps[1] + 12, ps[0] + 7]
    for j, p in enumerate(pat * 1):
        s.note(4, bt + j * 0.5, 0.9, p, 52 + (6 if j == 0 else 0))
    s.chord(2, bt, 2.05, [p + 12 for p in ps[:3]], vel=40 if bt < b(9) else 52)

# melody (top line), doubled by music box an octave up
mel = [(1.6, 'G4', 1), (2.6, 'Bb4', 1), (3.6, 'F4', 1.5), (5.1, 'Eb4', 0.5), (5.6, 'C5', 1), (6.6, 'Bb4', 1),
       (7.6, 'Ab4', 1.5), (9.1, 'G4', 0.5), (9.6, 'F4', 2),
       # dawn: the line lifts
       (11.6, 'G4', 0.5), (12.1, 'Bb4', 0.5), (12.6, 'Eb5', 1), (13.6, 'C5', 1), (14.6, 'Ab4', 1),
       (15.6, 'F4', 1), (16.6, 'G4', 0.5), (17.1, 'Ab4', 0.5), (17.6, 'Bb4', 1.5), (19.1, 'D5', 0.5),
       (19.6, 'Eb5', 2.5)]
for bt, n, d in mel:
    s.note(0, bt, d + 0.3, n, 62)
    s.note(1, bt, d + 0.6, NOTE(n) + 12, 54 if bt < b(9) else 48)
# dawn: strings swell in (9.0 s = beat 9.9)
s.swell(3, b(8.8), 4, 20, 100)
s.chord(3, b(8.9), 6.2, chord('Eb3', 'maj') + [NOTE('G4')], vel=58)
s.chord(3, b(8.9) + 6.2, 4.0, chord('F3', 'min7'), vel=58)
s.chord(3, b(8.9) + 10.2, 5.0, chord('Eb3', 'add9'), vel=60)
# glockenspiel on "forgotten"
s.inst(5, GM['glockenspiel'], vol=100, pan=70, reverb=110)
s.note(5, b(9.38), 3, 'Bb6', 92)
# clock ticks (woodblock) on every flip
s.inst(9, 0, vol=90, kit='standard', reverb=40)
for tt in (0.38, 2.0, 3.38, 4.68, 5.78, 7.38):
    s.drum(b(tt), 'woodblock_hi', 46)
import math
for i in range(1, 16):
    e = 0.5 - 0.5 * math.cos(math.pi * i / 15)
    s.drum(b(9.05 + 1.25 * e), 'woodblock_hi', 30)
s.drum(b(16.5), 'claves', 34)          # tap on the phone
s.drum(b(7.43), 'woodblock_lo', 60)    # the window latch
s.render('bed.wav', seconds=20.4, fade_out=1.0, gain=0.7)

# noise SFX
tr = fx.Track(20.4)
tr.add_wav(0, 'bed.wav', 1.0)
tr.add(2.2, fx.sweep_noise(0.7, 2400, 500), 0.20, -0.4)    # duvet off
tr.add(3.40, fx.sweep_noise(0.65, 500, 2000), 0.16, -0.3)  # duvet on
tr.add(4.72, fx.sweep_noise(0.45, 2800, 600), 0.20, -0.4)  # duvet off, faster
tr.add(5.86, fx.sweep_noise(0.5, 900, 1800), 0.10, 0.2)    # pillow flip
tr.add(7.40, fx.creak(0.7, 160), 0.12, -0.3)                 # window creak
tr.add(7.50, fx.wind(1.9), 0.13, -0.2)                       # cold air
tr.add(14.5, fx.sweep_noise(0.9, 400, 2200), 0.12, 0.0)    # phone rises
tr.write('mix_pre.wav', 20.0)
print('bed', loudness('bed.wav'), 'pre', loudness('mix_pre.wav'))
