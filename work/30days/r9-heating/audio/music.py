# R9 winter lullaby: celesta + soft strings + harp, D minor turning to F major, 72 bpm.
import sys, subprocess
sys.path.insert(0, '/home/claude/clari-media/work/kit/music')
from musiclib import Song, GM, NOTE, chord, loudness
s = Song(bpm=72)
b = s.beat_at                                   # seconds -> beats
s.inst(0, GM['celesta'], vol=96, pan=54, reverb=100, chorus=30)
s.inst(1, GM['harp'], vol=88, pan=78, reverb=95)
s.inst(2, GM['strings_slow'], vol=72, pan=60, reverb=110, chorus=40)
s.inst(3, GM['cello'], vol=62, pan=48, reverb=100)
s.inst(4, GM['glockenspiel'], vol=70, pan=70, reverb=110)
s.inst(5, GM['pad_warm'], vol=52, reverb=110, chorus=60)
s.inst(9, 0, vol=90, kit='orchestra')

T = [5.0, 7.6, 10.4, 13.4, 17.2]
# harmony: Dm | Dm/C | Bb (fire) | Bb | F/A | Gm | C | F (resolution)
sec = [(0.0, 'D3', 'min', 'D2'), (1.45, 'C3', 'min', 'A1'), (2.85, 'Bb2', 'maj9', 'Bb1'),
       (T[0], 'G2', 'min7', 'G1'), (T[1], 'F2', 'maj7', 'A1'), (T[2], 'G2', 'min9', 'G1'),
       (T[3], 'C3', 'sus4', 'C2'), (T[3] + 1.9, 'C3', '7', 'C2'), (T[4], 'F2', 'add9', 'F1')]
fix = {1: [NOTE('A2'), NOTE('D3'), NOTE('F3'), NOTE('C4')]}   # Dm/C colour
for i, (t0, root, kind, bass) in enumerate(sec):
    t1 = sec[i + 1][0] if i + 1 < len(sec) else 21.5
    ps = fix.get(i) or chord(root, kind)
    s.chord(2, b(t0), b(t1 - t0) + 0.4, [p + 12 for p in ps], vel=48 if t0 < 2.8 else 56)
    s.note(3, b(t0), b(t1 - t0) + 0.3, bass, vel=58)
    s.chord(5, b(t0), b(t1 - t0) + 0.4, ps, vel=40)
    # harp: rolling arpeggio, 8ths
    arp = [ps[0], ps[1] + 12 if len(ps) > 1 else ps[0] + 12, ps[2] + 12, ps[1] + 24 if len(ps) > 1 else ps[0] + 24]
    k, bt = 0, b(t0)
    while bt < b(t1) - 0.25:
        s.note(1, bt, 1.2, arp[k % 4], vel=50 if t0 < 2.8 else 58); k += 1; bt += 0.5

# celesta melody: a lullaby line, one phrase per beat of the story
mel = [  # (second, note, beats)
    (0.10, 'A5', 1), (0.95, 'F5', 0.5), (1.35, 'E5', 0.5), (1.75, 'D5', 1.5),
    (2.95, 'F5', 0.5), (3.35, 'A5', 0.5), (3.75, 'D6', 2),
    (5.10, 'D6', 1), (5.95, 'C6', 0.5), (6.35, 'Bb5', 1.5),
    (7.70, 'A5', 1), (8.55, 'C6', 0.5), (8.95, 'F5', 1.5),
    (10.5, 'Bb5', 1), (11.35, 'A5', 0.5), (11.75, 'G5', 1.5),
    (13.5, 'G5', 1), (14.35, 'C6', 0.5), (14.75, 'Bb5', 1), (15.8, 'E5', 1.5),
    (17.35, 'F5', 1), (18.2, 'A5', 1), (19.0, 'C6', 2.5),
]
for t0, n, d in mel: s.note(0, b(t0), d, n, vel=72)
# on fire: harp gliss up D minor into Bb
gl = ['D4', 'E4', 'F4', 'G4', 'A4', 'Bb4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'Bb5', 'D6']
for i, n in enumerate(gl): s.note(1, b(2.55) + i * 0.06, 1.5, n, vel=60 + i * 2)
s.swell(2, 0, b(2.85), 70, 96); s.swell(2, b(2.85), b(1.2), 96, 118); s.swell(2, b(4.4), b(1.0), 118, 100)
s.swell(2, b(T[4]), b(3.2), 100, 80)
# glock on "tonight"
s.note(4, b(T[4] + 0.42), 3, 'A6', 76); s.note(4, b(T[4] + 0.42), 3, 'F6', 50)
# dial clicks: wind-up tick then the click (woodblock hi); radiator ticks early on
for t0 in T:
    s.drum(b(t0 + 0.0), 'triangle_mute', 40)
    s.drum(b(t0 + 0.09), 'woodblock_hi', 92)
for t0 in (0.35, 0.95, 1.6, 2.3): s.drum(b(t0), 'claves', 34)
s.drum(b(1.67), 'tom_lo', 70)                 # duvet lands
s.render('bed.wav', seconds=21.0, fade_out=1.2, gain=0.75)
print('bed', loudness('bed.wav'))

# sfx: wind (filtered noise, swells at the frost), duvet whoosh
def run(a): subprocess.run(a, check=True)
run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anoisesrc=d=21:c=pink:r=48000:a=0.5',
     '-af', "lowpass=f=700,highpass=f=180,volume='0.18+0.22*between(t,17,21)*min((t-17)/2,1)':eval=frame,afade=t=out:st=19.5:d=1.5", '-ac', '2', 'wind.wav'])
run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anoisesrc=d=0.6:c=pink:r=48000:a=0.8',
     '-af', 'bandpass=f=900:w=1400,afade=t=in:d=0.35,afade=t=out:st=0.4:d=0.2', '-ac', '2', 'whoosh.wav'])
run(['ffmpeg', '-v', 'error', '-y', '-i', 'bed.wav', '-i', 'wind.wav', '-i', 'whoosh.wav', '-i', 'whoosh.wav', '-filter_complex',
     '[2]adelay=1150|1150,volume=0.9[w1];[3]adelay=2950|2950,volume=0.7[w2];[0][1][w1][w2]amix=inputs=4:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11',
     '-ar', '48000', 'mix.wav'])
print('mix', loudness('mix.wav'))
