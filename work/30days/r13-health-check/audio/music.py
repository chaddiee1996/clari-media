# R13: hopeful morning. Acoustic steel guitar + flute in G major, 98 bpm. SFX: letterbox clack, envelope tear.
import sys, subprocess
sys.path.insert(0, '/home/claude/clari-media/work/kit/music')
from musiclib import Song, GM, NOTE, chord, loudness
s = Song(bpm=98); b = s.beat_at
s.inst(0, GM['steel_guitar'], vol=86, pan=46, reverb=70)
s.inst(1, GM['flute'], vol=76, pan=74, reverb=95)
s.inst(2, GM['strings_slow'], vol=56, pan=60, reverb=110)
s.inst(3, GM['acoustic_bass'], vol=72, pan=56, reverb=40)
s.inst(4, GM['glockenspiel'], vol=64, pan=80, reverb=100)
s.inst(9, 0, vol=90, kit='standard')
END = 24.5
prog = [(0.0, 'G2', 'add9'), (2.45, 'D2', 'sus4'), (3.9, 'E2', 'min7'), (6.5, 'C3', 'maj7'), (9.0, 'D2', 'sus4'),
        (10.4, 'G2', 'maj7'), (12.9, 'E2', 'min7'), (13.3, 'C3', 'add9'), (15.3, 'D2', 'maj'), (16.7, 'E2', 'min7'),
        (19.0, 'C3', 'maj7'), (20.2, 'A2', 'min7'), (21.6, 'D2', 'sus4'), (22.3, 'G2', 'add9')]
for i, (t0, root, kind) in enumerate(prog):
    t1 = prog[i + 1][0] if i + 1 < len(prog) else END
    ps = chord(root, kind)
    s.note(3, b(t0), b(t1 - t0) * 0.6, ps[0], vel=62)
    s.chord(2, b(t0), b(t1 - t0) + 0.3, [p + 12 for p in ps[:3]], vel=40 if t0 > 3 else 34)
    # fingerpicked guitar: bass, then a rolling pattern on the upper strings, 8ths
    pat = [ps[0] + 12, ps[2] + 12, ps[1] + 24, ps[2] + 12, ps[-1] + 12, ps[2] + 12]
    k, bt = 0, b(t0)
    while bt < b(t1) - 0.2:
        s.note(0, bt, 0.9, pat[k % len(pat)], vel=52 + (8 if k % 6 == 0 else 0)); k += 1; bt += 0.5
s.swell(2, 0, b(4), 70, 96); s.swell(2, b(13.3), b(2.4), 96, 116); s.swell(2, b(20.2), b(2.2), 100, 118)
# flute: phrases in the gaps of the voice (2.5 to 3.9, 9.0 to 10.4, 12.3 to 13.2, 19.2 to 20.1, after 22.9)
for t0, n, d in [(0.2, 'D5', 1.5), (2.55, 'B5', 0.6), (2.95, 'A5', 0.6), (3.35, 'G5', 1.2),
                 (9.1, 'E5', 0.6), (9.5, 'F#5', 0.6), (9.9, 'G5', 1.4), (12.4, 'A5', 0.5), (12.75, 'B5', 1.0),
                 (19.25, 'D6', 0.6), (19.6, 'B5', 1.0), (22.9, 'B5', 0.8), (23.3, 'D6', 2.4)]:
    s.note(1, b(t0), d, n, vel=70)
# glock on the new line writing and on "count"
s.note(4, b(7.76), 2, 'D7', 60); s.note(4, b(9.3), 1.5, 'G6', 56); s.note(4, b(22.68), 3, 'B6', 60)
# letterbox clack: flap snaps shut at 2.4 s (woodblock low + rim), drop thump on the mat at 3.3
s.drum(b(0.35), 'rim', 40); s.drum(b(2.42), 'woodblock_lo', 100); s.drum(b(2.42), 'rim', 70); s.drum(b(3.35), 'tom_lo', 46)
s.render('bed.wav', seconds=END, fade_out=1.4, gain=0.72)
def run(a): subprocess.run(a, check=True)
# envelope tear: a crackly band-passed noise burst at 3.95 s
run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anoisesrc=d=0.5:c=white:r=48000:a=0.7',
     '-af', "highpass=f=1800,lowpass=f=7000,volume='0.5+0.5*sin(2*PI*t*37)':eval=frame,afade=t=in:d=0.05,afade=t=out:st=0.25:d=0.25", '-ac', '2', 'tear.wav'])
vo = '/home/claude/clari-media/work/30days/vo/R13.mp3'
run(['ffmpeg', '-v', 'error', '-y', '-i', vo, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', '-ac', '2', 'vo.wav'])
g = -16 - loudness('vo.wav')
run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo.wav', '-af', f'volume={g:.2f}dB', 'vo2.wav']); run(['mv', 'vo2.wav', 'vo.wav'])
run(['ffmpeg', '-v', 'error', '-y', '-i', 'bed.wav', '-i', 'tear.wav', '-filter_complex', '[1]adelay=3950|3950,volume=0.6[t];[0][t]amix=inputs=2:normalize=0,loudnorm=I=-28:TP=-8:LRA=11', '-ar', '48000', 'bed_n.wav'])
run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo.wav', '-i', 'bed_n.wav', '-filter_complex',
     '[0]apad=whole_dur=24.3[v];[v][1]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89', '-ar', '48000', 'mix.wav'])
print('vo', loudness('vo.wav'), 'bed', loudness('bed_n.wav'), 'mix', loudness('mix.wav'))
