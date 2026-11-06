# R3 "Why did I come upstairs?": playful pizzicato strings + marimba in F major, 112 bpm, bassoon "huh?" at each stair.
# Arc: a questioning motif, a marimba run down for the whip, one stair per phrase climbing up the scale,
# a soft tremolo turn for brain fog, back to the groove for the close, ending on F add9.
import sys; sys.path.insert(0, '/home/claude/clari-media/work/kit/music'); sys.path.insert(0, '.')
from musiclib import Song, GM, NOTE, chord, loudness
import sfxlib as fx

BPM = 112; b = lambda s: s * BPM / 60.0
D = 21.6
STEP = [3.0, 5.3, 7.6, 10.2, 12.6]; TURN = 14.6; CLOSE = 19.0
s = Song(bpm=BPM)
s.inst(0, GM['marimba'], vol=100, pan=70, reverb=55)
s.inst(1, GM['pizzicato'], vol=100, pan=50, reverb=60)
s.inst(2, GM['bassoon'], vol=96, pan=64, reverb=50)
s.inst(3, GM['pizzicato'], vol=80, pan=80, reverb=60)
s.inst(9, 0, vol=100, kit='standard', reverb=30)

# hook: a question that goes up and does not land
for bt, n in ((0.3, 'F5'), (0.8, 'A5'), (1.3, 'C6'), (1.8, 'D6')):
    s.note(0, bt, 0.6, n, 72)
s.note(1, 0.3, 1, 'F2', 70); s.note(1, 1.3, 1, 'C3', 64)
s.note(2, b(1.55), 0.35, 'C3', 70); s.note(2, b(1.55) + 0.4, 0.8, 'F3', 76)    # huh?
# whip down: marimba run
run = ['F6', 'D6', 'C6', 'A5', 'G5', 'F5', 'D5', 'C5', 'A4', 'F4']
for i, n in enumerate(run): s.note(0, b(2.3) + i * 0.16, 0.3, n, 70 - i * 2)

# one phrase per stair
CH = [('F', 'maj', 'F2'), ('G', 'min7', 'G2'), ('A', 'min7', 'A2'), ('Bb', 'maj7', 'Bb2'), ('C', 'sus4', 'C3')]
MEL = [['A5', 'C6', 'A5', 'F5'], ['Bb5', 'D6', 'Bb5', 'G5'], ['C6', 'E6', 'C6', 'A5'], ['D6', 'F6', 'D6', 'Bb5'], ['F6', 'G6', 'F6', 'C6']]
for k, t0 in enumerate(STEP):
    t1 = STEP[k + 1] if k + 1 < len(STEP) else TURN
    b0, b1 = b(t0), b(t1)
    root, kind, bass = CH[k]
    ps = chord(root + '4', kind)
    bt = b0; j = 0
    while bt < b1 - 0.2:
        if j % 2 == 0: s.note(1, bt, 0.5, NOTE(bass) + (7 if j % 4 == 2 else 0), 78)
        else: s.chord(3, bt, 0.4, ps, vel=56)
        bt += 1; j += 1
    # marimba line, tiptoe rhythm
    for i, n in enumerate(MEL[k]):
        s.note(0, b0 + 0.5 + i * 0.5, 0.45, n, 66)
    s.note(0, b0 + 2.75, 0.4, MEL[k][1], 54)
    # footstep (low tom) as the camera lands on the stair, the object "tok", the bassoon "huh?"
    s.drum(b(t0 + 0.42), 'tom_lo', 74)
    if k < 4: s.drum(b(t0 + 0.59), 'woodblock_lo', 88)
    hp = NOTE(bass) + 12
    s.note(2, b(t0 + 0.78), 0.3, hp, 64); s.note(2, b(t0 + 0.78) + 0.33, 0.7, hp + 5, 72)

# the turn: soft marimba tremolo on Bbmaj7 then Dm7, pizz pedal
for name, kind, start, end in (('Bb3', 'maj7', TURN, TURN + 2.4), ('D4', 'min7', TURN + 2.4, CLOSE)):
    ps = chord(name, kind); bt = b(start)
    while bt < b(end) - 0.1:
        for p in ps[1:]: s.note(0, bt, 0.2, p + 12, 34)
        bt += 0.25
    s.note(1, b(start), 2, NOTE(name) - 12, 54)
# the close: groove back in F, ends on F add9
bt = b(CLOSE); j = 0
while bt < b(D - 1.2):
    if j % 2 == 0: s.note(1, bt, 0.5, NOTE('F2') + (7 if j % 4 == 2 else 0), 70)
    else: s.chord(3, bt, 0.4, chord('F4', 'maj'), vel=50)
    bt += 1; j += 1
for i, n in enumerate(['C6', 'A5', 'F5', 'G5', 'A5', 'C6']): s.note(0, b(CLOSE) + 0.5 + i * 0.5, 0.45, n, 62)
s.chord(0, b(D - 1.3), 3, chord('F4', 'add9'), vel=56, strum=0.05)
s.note(1, b(D - 1.3), 2, 'F2', 66)
s.render('bed.wav', seconds=D + 0.2, fade_out=1.0, gain=0.7)

tr = fx.Track(D + 0.2)
tr.add_wav(0, 'bed.wav', 1.0)
tr.add(2.3, fx.sweep_noise(0.85, 3000, 500), 0.16, 0.0)     # the whip down the stairs
tr.add(TURN, fx.sweep_noise(1.2, 500, 1800), 0.08, 0.0)    # pull back
tr.write('mix_pre.wav', D)
print('bed', loudness('bed.wav'), 'pre', loudness('mix_pre.wav'))
