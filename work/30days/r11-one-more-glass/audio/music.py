# R11: festive but soft brushed jazz trio in G, 104 bpm swing. Jazz guitar comping, upright bass, brushes,
# vibraphone melody. SFX: two glasses clink, party murmur kept very low.
import sys, subprocess
sys.path.insert(0, '/home/claude/clari-media/work/kit/music')
from musiclib import Song, GM, NOTE, chord, loudness
s = Song(bpm=104); b = s.beat_at
s.inst(0, GM['jazz_guitar'], vol=80, pan=44, reverb=60)
s.inst(1, GM['acoustic_bass'], vol=100, pan=60, reverb=40)
s.inst(2, GM['vibraphone'], vol=90, pan=78, reverb=85, chorus=30)
s.inst(3, GM['glockenspiel'], vol=80, pan=90, reverb=100)
s.inst(9, 0, vol=80, kit='brush')
SW = 0.66   # swung off-beat position inside a beat
# two bars per line: (bar, chord root, kind) ; 4 beats per bar
prog = [('A2', 'min7'), ('D2', '7'), ('G2', 'maj7'), ('E2', '7'),
        ('A2', 'min7'), ('D2', '7'), ('B2', 'min7'), ('E2', '7'),
        ('C3', 'maj7'), ('C3', 'min6'), ('B2', 'min7'), ('E2', '7'),
        ('A2', 'min7'), ('D2', '7'), ('G2', 'maj9'), ('G2', 'maj9')]
# 2 beats per chord -> 32 beats ~ 18.5 s, then a held G on the end
END_B = b(20.8)
thin = lambda bt: b(5.4) <= bt < b(9.8)
for i, (root, kind) in enumerate(prog):
    bt0 = i * 2 + b(0.0)
    ps = chord(root, kind)
    # walking bass: root, 3rd/5th, approach
    walk = [ps[0], ps[2] if i % 2 else ps[1], ps[0] + 12, ps[0] + 10]
    for k in range(2):
        s.note(1, bt0 + k, 0.9, walk[(k * 2 + i) % 4], vel=82 if k == 0 else 72)
    # guitar comp: Freddie Green on 1, a swung stab on the and-of-2
    voic = [p + 12 for p in ps[1:4]] if len(ps) > 3 else [p + 12 for p in ps]
    s.chord(0, bt0, 0.5, voic, vel=58, strum=0.012)
    if not thin(bt0): s.chord(0, bt0 + 1 + SW, 0.35, voic, vel=50, strum=0.012)
    # brushes: swish on 2 and 4 (snare2 = brush slap), ride-ish pattern on the hat
    s.drum(bt0 + 1, 'snare', 34 if thin(bt0) else 48)
    for k in range(2):
        s.drum(bt0 + k, 'ride', 30); s.drum(bt0 + k + SW, 'pedal_hat', 26)
# held ending chord
s.chord(0, 32, 4, [NOTE('B3'), NOTE('D4'), NOTE('F#4'), NOTE('A4')], vel=54, strum=0.04)
s.note(1, 32, 4, 'G1', 80)
# vibes melody (beats), swung, phrases answer the picture
mel = [(0.1, 'B4', 0.6), (0.1 + SW + 0.5, 'D5', 0.4), (1.5, 'E5', 0.9), (2.66, 'D5', 0.4), (3.0, 'B4', 1.2),
       (4.66, 'A4', 0.4), (5.0, 'C5', 0.5), (5.66, 'E5', 0.4), (6.0, 'G5', 1.4),          # "Here it comes" lifts
       (7.66, 'F#5', 0.4), (8.0, 'E5', 0.6), (9.0, 'D5', 2.0),
       (17.0, 'G5', 0.6), (17.66, 'E5', 0.4), (18.0, 'D5', 0.6), (19.0, 'B4', 1.5),        # "noticing"
       (23.0, 'A4', 0.6), (23.66, 'B4', 0.4), (24.0, 'D5', 0.8), (25.0, 'E5', 1.6),
       (29.0, 'F#5', 0.6), (29.66, 'E5', 0.4), (30.0, 'D5', 0.6), (31.0, 'B4', 0.6), (32.0, 'D5', 3.5)]
for bt, n, d in mel: s.note(2, bt, d, n, vel=70)
# "Here it comes": vibes run up and a soft cymbal swell
for i, n in enumerate(['G4', 'A4', 'B4', 'D5', 'E5', 'G5', 'A5', 'B5']): s.note(2, b(2.75) + i * 0.09, 0.8, n, 58 + i * 3)
s.drum(b(3.0), 'crash', 40)
# clink: two glass notes slightly apart (glockenspiel) + triangle
for dt, n in ((0.0, 'E7'), (0.035, 'B6')): s.note(3, b(1.56 + dt), 1.6, n, 92)
s.drum(b(1.56), 'triangle', 60)
s.render('bed.wav', seconds=21.0, fade_out=1.0, gain=0.75)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anoisesrc=d=21:c=brown:r=48000:a=0.6',
                '-af', "bandpass=f=520:w=700,tremolo=f=1.3:d=0.4,volume=0.08,afade=t=in:d=1,afade=t=out:st=13:d=3", '-ac', '2', 'murmur.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'bed.wav', '-i', 'murmur.wav', '-filter_complex',
                '[0][1]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', 'mix.wav'], check=True)
print('bed', loudness('bed.wav'), 'mix', loudness('mix.wav'))
