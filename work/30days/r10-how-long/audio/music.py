# R10: reflective, moving forward. Piano arpeggios in B flat major, 92 bpm, slow string swells,
# a clock-like woodblock pulse under the years. Thin under the voice.
import sys, subprocess
sys.path.insert(0, '/home/claude/clari-media/work/kit/music')
from musiclib import Song, GM, NOTE, chord, loudness
s = Song(bpm=92); b = s.beat_at
s.inst(0, GM['grand_piano'], vol=86, pan=58, reverb=90)
s.inst(1, GM['strings_slow'], vol=70, pan=66, reverb=110, chorus=40)
s.inst(2, GM['cello'], vol=60, pan=50, reverb=100)
s.inst(3, GM['celesta'], vol=60, pan=74, reverb=110)
s.inst(9, 0, vol=80, kit='orchestra')
# (start s, root, kind, bass)
prog = [(0.0, 'Bb3', 'add9', 'Bb1'), (2.6, 'G3', 'min7', 'G1'), (4.3, 'Eb3', 'maj7', 'Eb2'), (6.0, 'F3', 'sus4', 'F1'),
        (7.0, 'F3', 'maj', 'F1'), (8.1, 'G3', 'min9', 'G1'), (10.4, 'Eb3', 'maj9', 'Eb2'), (12.2, 'C3', 'min7', 'C2'),
        (14.3, 'F3', 'sus4', 'F1'), (15.5, 'Eb3', 'add9', 'Eb2'), (17.5, 'C3', 'min9', 'C2'), (19.2, 'F3', '7', 'F1'),
        (20.9, 'Eb3', 'maj7', 'Eb2'), (22.2, 'F3', 'sus4', 'F2'), (22.86, 'Bb3', 'add9', 'Bb1')]
END = 25.5
for i, (t0, root, kind, bass) in enumerate(prog):
    t1 = prog[i + 1][0] if i + 1 < len(prog) else END
    ps = chord(root, kind)
    s.chord(1, b(t0), b(t1 - t0) + 0.5, [p + 12 for p in ps[:3]], vel=46)
    s.note(2, b(t0), b(t1 - t0) + 0.3, bass, vel=52)
    # piano arpeggio, 8ths, up then down; denser through the years (4.3 to 8), sparse under the dense voice
    pat = [ps[0], ps[1] + 12, ps[2] + 12, ps[0] + 24, ps[2] + 12, ps[1] + 12]
    step = 0.5 if (4.3 <= t0 < 8.1 or t0 >= 20.9) else 1.0
    k, bt = 0, b(t0)
    while bt < b(t1) - 0.2:
        s.note(0, bt, 1.4, pat[k % len(pat)], vel=50 + (6 if k % 3 == 0 else 0)); k += 1; bt += step
s.swell(1, 0, b(8), 60, 92); s.swell(1, b(8), b(7), 92, 80); s.swell(1, b(15.5), b(5), 80, 100); s.swell(1, b(20.9), b(2.5), 100, 120)
# clock pulse under the years, speeding up with the moons
t, gapv = 4.3, 0.65
while t < 8.0:
    s.drum(b(t), 'woodblock_lo' if int((t - 4.3) / 0.65) % 2 else 'woodblock_hi', 46); t += gapv; gapv = max(0.2, gapv * 0.86)
# celesta sparkle on the label changes and on "speak"
for t0, n in ((8.64, 'D6'), (12.44, 'F6'), (13.32, 'G6'), (22.86, 'F6'), (22.86, 'D7')): s.note(3, b(t0), 2, n, 64)
s.render('bed.wav', seconds=25.0, fade_out=1.3, gain=0.7)
vo = '/home/claude/clari-media/work/30days/vo/R10.mp3'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vo, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', '-ac', '2', 'vo.wav'], check=True)
g = -16 - loudness('vo.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo.wav', '-af', f'volume={g:.2f}dB', 'vo2.wav'], check=True); subprocess.run(['mv', 'vo2.wav', 'vo.wav'])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'bed.wav', '-af', 'loudnorm=I=-28:TP=-8:LRA=11', '-ar', '48000', 'bed_n.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo.wav', '-i', 'bed_n.wav', '-filter_complex',
                '[0]apad=whole_dur=25[v];[v][1]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.89', '-ar', '48000', 'mix.wav'], check=True)
print('vo', loudness('vo.wav'), 'bed', loudness('bed_n.wav'), 'mix', loudness('mix.wav'))
