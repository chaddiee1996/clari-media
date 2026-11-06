"""Clari music kit: write music as notes, render with real sampled instruments.

Instruments come from FluidR3_GM.sf2 (MIT licence, Frank Wen), rendered by FluidSynth.
Usage in a reel's music.py:

    import sys; sys.path.insert(0, '/home/claude/clari-media/work/kit/music')
    from musiclib import Song, GM, chord, NOTE
    s = Song(bpm=72)
    s.inst(0, GM['felt_piano'])            # channel 0 = piano
    s.inst(1, GM['strings_slow'], vol=70)  # channel 1 = strings
    s.note(0, beat=0, dur=1, pitch=NOTE('C5'), vel=70)
    s.chord(1, beat=0, dur=4, pitches=chord('A3', 'min7'), vel=50)
    s.drum(beat=0, kit_note=36, vel=80)   # channel 9 drums (kit 0 standard, 40 brush, 8 room)
    s.render('bed.wav', seconds=22)         # 48 kHz stereo, reverb + chorus on, trimmed/faded

Rules: every reel gets its own key, tempo, instruments and melody. Keep the bed quiet and spacious
under voice (fewer notes, long pads); text-only reels can carry a real melody.
"""
import subprocess, os, tempfile, math
import mido

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'

# General MIDI program numbers (0-based) that sound good in FluidR3
GM = {
    'grand_piano': 0, 'bright_piano': 1, 'felt_piano': 0, 'rhodes': 4, 'ep2': 5, 'harpsichord': 6,
    'celesta': 8, 'glockenspiel': 9, 'music_box': 10, 'vibraphone': 11, 'marimba': 12, 'xylophone': 13,
    'tubular_bells': 14, 'dulcimer': 15, 'organ_soft': 19, 'accordion': 21,
    'nylon_guitar': 24, 'steel_guitar': 25, 'jazz_guitar': 26, 'clean_guitar': 27,
    'acoustic_bass': 32, 'finger_bass': 33, 'fretless_bass': 35, 'synth_bass': 38,
    'violin': 40, 'viola': 41, 'cello': 42, 'contrabass': 43, 'tremolo_strings': 44, 'pizzicato': 45,
    'harp': 46, 'timpani': 47, 'strings': 48, 'strings_slow': 49, 'synth_strings': 50,
    'choir_aah': 52, 'voice_ooh': 53, 'orchestra_hit': 55,
    'trumpet': 56, 'muted_trumpet': 59, 'french_horn': 60, 'brass': 61,
    'soprano_sax': 64, 'alto_sax': 65, 'tenor_sax': 66, 'oboe': 68, 'english_horn': 69, 'bassoon': 70,
    'clarinet': 71, 'piccolo': 72, 'flute': 73, 'recorder': 74, 'pan_flute': 75, 'bottle': 76,
    'whistle': 78, 'ocarina': 79, 'square_lead': 80, 'saw_lead': 81, 'calliope': 82,
    'pad_new_age': 88, 'pad_warm': 89, 'pad_poly': 90, 'pad_choir': 91, 'pad_bowed': 92,
    'pad_metal': 93, 'pad_halo': 94, 'pad_sweep': 95, 'fx_crystal': 98, 'fx_atmos': 99,
    'fx_bright': 100, 'fx_echo': 102, 'sitar': 104, 'banjo': 105, 'kalimba': 108,
    'steel_drum': 114, 'woodblock': 115, 'taiko': 116, 'melodic_tom': 117,
    'fx_breath': 121, 'fx_seashore': 122, 'fx_bird': 123, 'fx_phone': 124, 'fx_applause': 126,
}
# drum kits (bank 128 program): standard 0, room 8, power 16, electronic 24, jazz 32, brush 40, orchestra 48
KITS = {'standard': 0, 'room': 8, 'jazz': 32, 'brush': 40, 'orchestra': 48}
# useful kit notes
DR = {'kick': 36, 'rim': 37, 'snare': 38, 'clap': 39, 'snare2': 40, 'hat': 42, 'hat_open': 46, 'pedal_hat': 44,
      'tom_lo': 45, 'tom_mid': 47, 'tom_hi': 50, 'crash': 49, 'ride': 51, 'ride_bell': 53, 'tamb': 54,
      'cowbell': 56, 'shaker': 70, 'cabasa': 69, 'triangle': 81, 'triangle_mute': 80, 'claves': 75,
      'woodblock_hi': 76, 'woodblock_lo': 77, 'bongo_hi': 60, 'bongo_lo': 61, 'conga': 63, 'brush_swirl': 40}

_NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def NOTE(n):
    """'C4' -> 60, 'F#3' -> 54, 'Bb5' -> 82"""
    p = _NAMES[n[0].upper()]; i = 1
    while i < len(n) and n[i] in '#b':
        p += 1 if n[i] == '#' else -1; i += 1
    return p + 12 * (int(n[i:]) + 1)

CH = {'maj': [0, 4, 7], 'min': [0, 3, 7], 'maj7': [0, 4, 7, 11], 'min7': [0, 3, 7, 10], '7': [0, 4, 7, 10],
      'sus2': [0, 2, 7], 'sus4': [0, 5, 7], 'add9': [0, 4, 7, 14], 'madd9': [0, 3, 7, 14], 'maj9': [0, 4, 7, 11, 14],
      'min9': [0, 3, 7, 10, 14], '6': [0, 4, 7, 9], 'min6': [0, 3, 7, 9], 'dim': [0, 3, 6], '5': [0, 7, 12]}
def chord(root, kind='maj', inv=0):
    r = NOTE(root) if isinstance(root, str) else root
    ps = [r + i for i in CH[kind]]
    for _ in range(inv): ps = ps[1:] + [ps[0] + 12]
    return ps

class Song:
    def __init__(self, bpm=80, tpb=480):
        self.bpm, self.tpb = bpm, tpb
        self.ev = []          # (tick, order, channel, msg)
        self.progs = {}
    def b2t(self, beat): return int(round(beat * self.tpb))
    def sec(self, beat): return beat * 60.0 / self.bpm
    def beat_at(self, seconds): return seconds * self.bpm / 60.0
    def inst(self, ch, program, vol=100, pan=64, reverb=60, chorus=20, kit=None):
        """set instrument on a channel (0-15, 9 = drums). pan 0 left .. 127 right"""
        msgs = []
        if ch == 9 or kit is not None:
            msgs.append(mido.Message('control_change', channel=ch, control=0, value=1 if ch != 9 else 0))
            program = KITS.get(kit, kit or 0) if isinstance(kit, str) else (kit or 0)
        msgs.append(mido.Message('program_change', channel=ch, program=program))
        for c, v in ((7, vol), (10, pan), (91, reverb), (93, chorus)):
            msgs.append(mido.Message('control_change', channel=ch, control=c, value=int(v)))
        for m in msgs: self.ev.append((0, 0, ch, m))
    def note(self, ch, beat, dur, pitch, vel=80):
        p = NOTE(pitch) if isinstance(pitch, str) else int(pitch)
        t0, t1 = self.b2t(beat), self.b2t(beat + dur)
        self.ev.append((t0, 2, ch, mido.Message('note_on', channel=ch, note=p, velocity=max(1, min(127, int(vel))))))
        self.ev.append((max(t1, t0 + 1), 1, ch, mido.Message('note_off', channel=ch, note=p, velocity=0)))
    def chord(self, ch, beat, dur, pitches, vel=70, strum=0.0):
        for i, p in enumerate(pitches): self.note(ch, beat + i * strum, dur - i * strum, p, vel)
    def drum(self, beat, kit_note, vel=80, dur=0.25):
        n = DR.get(kit_note, kit_note) if isinstance(kit_note, str) else kit_note
        self.note(9, beat, dur, n, vel)
    def cc(self, ch, beat, control, value):
        self.ev.append((self.b2t(beat), 0, ch, mido.Message('control_change', channel=ch, control=control, value=int(value))))
    def swell(self, ch, beat, dur, v0, v1, steps=24, control=11):
        """expression ramp (CC11) for fades and swells"""
        for i in range(steps + 1):
            self.cc(ch, beat + dur * i / steps, control, v0 + (v1 - v0) * i / steps)
    def write_mid(self, path):
        mid = mido.MidiFile(ticks_per_beat=self.tpb); tr = mido.MidiTrack(); mid.tracks.append(tr)
        tr.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(self.bpm)))
        last = 0
        for tick, _, ch, m in sorted(self.ev, key=lambda e: (e[0], e[1])):
            tr.append(m.copy(time=tick - last)); last = tick
        mid.save(path)
    def render(self, out_wav, seconds=None, gain=0.6, fade_out=1.5, fade_in=0.0, sf2=SF2, room=0.6, width=0.8, level=0.5):
        """render to 48 kHz stereo WAV with FluidSynth reverb. seconds trims the file (with fade_out)."""
        d = tempfile.mkdtemp(); mp = os.path.join(d, 'm.mid'); raw = os.path.join(d, 'r.wav')
        self.write_mid(mp)
        subprocess.run(['fluidsynth', '-ni', '-q', '-r', '48000', '-g', str(gain),
                        '-o', 'synth.reverb.active=1', '-o', f'synth.reverb.room-size={room}',
                        '-o', f'synth.reverb.width={width}', '-o', f'synth.reverb.level={level}',
                        '-o', 'synth.chorus.active=1', '-F', raw, sf2, mp], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        af = []
        if fade_in: af.append(f'afade=t=in:d={fade_in}')
        if seconds:
            af.append(f'atrim=0:{seconds}')
            if fade_out: af.append(f'afade=t=out:st={max(0, seconds - fade_out)}:d={fade_out}')
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', raw]
        if af: cmd += ['-af', ','.join(af)]
        cmd += ['-ar', '48000', '-ac', '2', out_wav]
        subprocess.run(cmd, check=True)
        return out_wav

def loudness(path):
    """integrated LUFS of a file (for checking a mix you cannot hear)"""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'ebur128', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    for line in reversed(r.splitlines()):
        if line.strip().startswith('I:'): return float(line.split()[1])
    return None
