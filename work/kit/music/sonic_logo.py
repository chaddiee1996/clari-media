# The Clari sound logo. Same on every reel: celesta + harp motif rising to a soft D major add9 chord.
import sys; sys.path.insert(0, '.')
from musiclib import Song, GM, NOTE, chord
s = Song(bpm=120)
s.inst(0, GM['celesta'], vol=100, pan=58, reverb=90)
s.inst(1, GM['harp'], vol=92, pan=74, reverb=90)
s.inst(2, GM['pad_warm'], vol=62, reverb=100, chorus=50)
s.inst(3, GM['strings_slow'], vol=55, reverb=100)
for b, n in ((0.5, 'A5'), (1.4, 'D6'), (2.2, 'F#6')):
    s.note(0, b, 2.5, n, 78); s.note(1, b, 2.5, NOTE(n) - 12, 70)
s.chord(1, 3.0, 4, chord('D4', 'add9'), vel=62, strum=0.06)
s.note(0, 3.0, 4, 'A6', 64); s.note(0, 3.0, 4, 'E6', 50)
s.chord(2, 0.3, 6.5, chord('D3', 'add9'), vel=55)
s.chord(3, 2.8, 4.0, chord('D4', 'maj'), vel=45)
s.render('sonic_logo.wav', seconds=4.0, fade_out=1.2, gain=0.7)
