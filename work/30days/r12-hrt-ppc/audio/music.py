# R12: light and bright. Marimba + pizzicato in E flat, 100 bpm, glockenspiel sparkle as each month lights,
# a soft stamp when the certificate lands. Thin under the voice.
import sys, subprocess
sys.path.insert(0, '/home/claude/clari-media/work/kit/music')
from musiclib import Song, GM, NOTE, chord, loudness
s = Song(bpm=100); b = s.beat_at
s.inst(0, GM['marimba'], vol=88, pan=50, reverb=70)
s.inst(1, GM['pizzicato'], vol=84, pan=76, reverb=80)
s.inst(2, GM['glockenspiel'], vol=78, pan=84, reverb=100)
s.inst(3, GM['strings_slow'], vol=58, pan=60, reverb=110)
s.inst(4, GM['acoustic_bass'], vol=80, pan=56, reverb=40)
s.inst(9, 0, vol=90, kit='standard')
END = 24.0
prog = [(0.0, 'Eb3', 'add9'), (2.4, 'C3', 'min7'), (4.8, 'Ab2', 'maj7'), (7.2, 'Bb2', 'sus4'), (8.6, 'Bb2', '7'),
        (9.28, 'Eb3', 'maj9'), (11.26, 'Ab2', 'maj9'), (13.4, 'Bb2', 'sus4'), (14.5, 'Eb3', 'add9'),
        (16.9, 'C3', 'min7'), (19.3, 'Ab2', 'maj7'), (21.2, 'Bb2', 'sus4'), (22.2, 'Eb3', 'add9')]
for i, (t0, root, kind) in enumerate(prog):
    t1 = prog[i + 1][0] if i + 1 < len(prog) else END
    ps = chord(root, kind)
    s.chord(3, b(t0), b(t1 - t0) + 0.3, [p + 12 for p in ps[:3]], vel=40)
    s.note(4, b(t0), b(t1 - t0) * 0.5, ps[0] - 12, vel=60)
    # marimba: a light bouncing figure on 8ths (root, fifth, ninth/third)
    pat = [ps[0] + 24, ps[2] + 12, ps[-1] + 12, ps[2] + 12]
    k, bt = 0, b(t0)
    while bt < b(t1) - 0.2:
        if k % 4 != 3: s.note(0, bt, 0.45, pat[k % 4], vel=48 + (8 if k % 4 == 0 else 0))
        k += 1; bt += 0.5
    # pizzicato on the off-beats, a little answer
    bt = b(t0) + 1
    while bt < b(t1) - 0.3:
        s.note(1, bt, 0.3, ps[1] + 12, vel=46); bt += 2
# the price: a bright marimba run up into it
for i, n in enumerate(['Bb4', 'C5', 'D5', 'Eb5', 'F5', 'G5', 'Bb5', 'Eb6']): s.note(0, b(9.0) + i * 0.12, 0.6, n, 64 + i * 3)
s.note(2, b(10.0), 2, 'G6', 74); s.note(2, b(10.0), 2, 'Eb7', 54)
# twelve months: one glock note each, climbing the E flat scale
scale = ['Eb6', 'F6', 'G6', 'Ab6', 'Bb6', 'C7', 'D7', 'Eb7', 'F7', 'G7', 'Ab7', 'Bb7']
for i, n in enumerate(scale): s.note(2, b(11.3 + i * 0.205), 1.2, NOTE(n) - 12, 66)
# the stamp: soft kick + low tom + a short string swell before it
s.drum(b(14.5), 'kick', 92); s.drum(b(14.5), 'tom_lo', 70); s.swell(3, b(13.4), b(1.1), 70, 112); s.swell(3, b(14.6), b(1.5), 112, 90)
s.note(2, b(22.22), 3, 'Bb6', 60); s.note(2, b(22.22), 3, 'Eb7', 50)
s.render('bed.wav', seconds=END, fade_out=1.4, gain=0.7)
vo = '/home/claude/clari-media/work/30days/vo/R12.mp3'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vo, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', '-ac', '2', 'vo.wav'], check=True)
g = -16 - loudness('vo.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo.wav', '-af', f'volume={g:.2f}dB', 'vo2.wav'], check=True); subprocess.run(['mv', 'vo2.wav', 'vo.wav'])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'bed.wav', '-af', 'loudnorm=I=-28:TP=-8:LRA=11', '-ar', '48000', 'bed_n.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo.wav', '-i', 'bed_n.wav', '-filter_complex',
                '[0]apad=whole_dur=23.8[v];[v][1]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89', '-ar', '48000', 'mix.wav'], check=True)
print('vo', loudness('vo.wav'), 'bed', loudness('bed_n.wav'), 'mix', loudness('mix.wav'))
